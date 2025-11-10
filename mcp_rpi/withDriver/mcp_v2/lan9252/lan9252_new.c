#include <linux/module.h>
#include <linux/spi/spi.h>
#include <linux/delay.h>
#include <linux/device.h>
#include <linux/kernel.h>
#include <linux/sysfs.h>
#include <linux/mutex.h>
#include <linux/types.h>
#include <linux/timer.h>
#include <linux/jiffies.h>
#include <linux/workqueue.h>

#define DRIVER_NAME "lan9252"

/* LAN9252 Register Definitions */
#define RESET_CTL               0x01F8
#define ECAT_CSR_DATA           0x0300
#define ECAT_CSR_CMD            0x0304
#define ECAT_PRAM_RD_ADDR_LEN   0x0308
#define ECAT_PRAM_RD_CMD        0x030C
#define ECAT_PRAM_WR_ADDR_LEN   0x0310
#define ECAT_PRAM_WR_CMD        0x0314
#define BYTE_TEST               0x0064
#define HW_CFG                  0x0074
#define WDOG_STATUS             0x0440
#define AL_STATUS_REG_0         0x0130

/* LAN9252 Flags */
#define ECAT_CSR_BUSY           0x80
#define PRAM_READ_AVAIL         0x01
#define PRAM_WRITE_AVAIL        0x01
#define READY                   0x08000000
#define DIGITAL_RST             0x00000001
#define ETHERCAT_RST            0x00000040

/* EtherCAT State Machine States */
#define ESM_INIT                0x01
#define ESM_PREOP               0x02
#define ESM_BOOT                0x03
#define ESM_SAFEOP              0x04
#define ESM_OP                  0x08

/* ESC Commands */
#define ESC_WRITE               0x80
#define ESC_READ                0xC0

/* SPI Commands */
#define COMM_SPI_READ           0x03
#define COMM_SPI_WRITE          0x02
#define DUMMY_BYTE              0xFF

/* Scan interval in milliseconds */
#define SCAN_INTERVAL_MS        10

/* Data Structures */
typedef union {
    uint16_t LANWord;
    uint8_t LANByte[2];
} UWORD;

typedef union {
    uint32_t LANLong;
    uint16_t LANWord[2];
    uint8_t LANByte[4];
} ULONG;

typedef union {
    uint8_t LANByte[32];
    uint32_t LANLong[8];
    float LANFloat[8];
} PROCBUFFER;

struct lan9252_data {
    struct spi_device *spi;
    struct mutex lock;
    struct timer_list scan_timer;
    struct work_struct scan_work;
    uint8_t operational;
    uint8_t watchdog_active;
    uint8_t last_status;
    PROCBUFFER buffer_out;
    PROCBUFFER buffer_in;
};

/* SPI Transfer Helper */
static int lan9252_spi_transfer(struct spi_device *spi, u8 *txbuf, u8 *rxbuf, size_t len)
{
    struct spi_transfer t = {
        .tx_buf = txbuf,
        .rx_buf = rxbuf,
        .len = len,
    };
    struct spi_message m;

    spi_message_init(&m);
    spi_message_add_tail(&t, &m);
    return spi_sync(spi, &m);
}

/* Read directly addressable register */
static uint32_t etc_read_reg(struct lan9252_data *dev, uint16_t address, uint8_t length)
{
    ULONG Result;
    UWORD Addr;
    uint8_t i;
    u8 tx_buf[7], rx_buf[7];
    int ret;

    Addr.LANWord = address;
    tx_buf[0] = COMM_SPI_READ;
    tx_buf[1] = Addr.LANByte[1];
    tx_buf[2] = Addr.LANByte[0];
    
    for (i = 0; i < length; i++) {
        tx_buf[i + 3] = DUMMY_BYTE;
    }

    mutex_lock(&dev->lock);
    ret = lan9252_spi_transfer(dev->spi, tx_buf, rx_buf, length + 3);
    mutex_unlock(&dev->lock);

    if (ret < 0) {
        dev_err(&dev->spi->dev, "SPI transfer failed: %d\n", ret);
        return 0;
    }

    Result.LANLong = 0;
    for (i = 0; i < length; i++) {
        Result.LANByte[i] = rx_buf[i + 3];
    }
    
    return Result.LANLong;
}

/* Write directly addressable register */
static void etc_write_reg(struct lan9252_data *dev, uint16_t address, uint32_t DataOut)
{
    ULONG Data;
    UWORD Addr;
    uint8_t i;
    u8 tx_buf[7], rx_buf[7];
    int ret;

    Addr.LANWord = address;
    Data.LANLong = DataOut;
    tx_buf[0] = COMM_SPI_WRITE;
    tx_buf[1] = Addr.LANByte[1];
    tx_buf[2] = Addr.LANByte[0];
    
    for (i = 0; i < 4; i++) {
        tx_buf[i + 3] = Data.LANByte[i];
    }

    mutex_lock(&dev->lock);
    ret = lan9252_spi_transfer(dev->spi, tx_buf, rx_buf, 7);
    mutex_unlock(&dev->lock);

    if (ret < 0) {
        dev_err(&dev->spi->dev, "SPI write failed: %d\n", ret);
    }
}

/* Read indirectly addressable register - non-blocking version */
static uint32_t etc_read_reg_wait_nb(struct lan9252_data *dev, uint16_t address, uint8_t length)
{
    ULONG TempLong;
    UWORD Addr;
    int timeout = 10; /* 10ms timeout */

    Addr.LANWord = address;
    TempLong.LANByte[0] = Addr.LANByte[0];
    TempLong.LANByte[1] = Addr.LANByte[1];
    TempLong.LANByte[2] = length;
    TempLong.LANByte[3] = ESC_READ;

    etc_write_reg(dev, ECAT_CSR_CMD, TempLong.LANLong);

    do {
        TempLong.LANLong = etc_read_reg(dev, ECAT_CSR_CMD, 4);
        if (!(TempLong.LANByte[3] & ECAT_CSR_BUSY))
            break;
        udelay(100); /* Use udelay instead of msleep */
        timeout--;
    } while (timeout > 0);

    if (timeout <= 0) {
        dev_err(&dev->spi->dev, "Timeout reading register 0x%04x\n", address);
        return 0;
    }

    TempLong.LANLong = etc_read_reg(dev, ECAT_CSR_DATA, length);
    return TempLong.LANLong;
}

/* Write indirectly addressable register - non-blocking version */
static void etc_write_reg_wait_nb(struct lan9252_data *dev, uint16_t address, uint32_t DataOut)
{
    ULONG TempLong;
    UWORD Addr;
    int timeout = 10; /* 10ms timeout */

    Addr.LANWord = address;
    etc_write_reg(dev, ECAT_CSR_DATA, DataOut);

    TempLong.LANByte[0] = Addr.LANByte[0];
    TempLong.LANByte[1] = Addr.LANByte[1];
    TempLong.LANByte[2] = 4;
    TempLong.LANByte[3] = ESC_WRITE;

    etc_write_reg(dev, ECAT_CSR_CMD, TempLong.LANLong);

    do {
        TempLong.LANLong = etc_read_reg(dev, ECAT_CSR_CMD, 4);
        if (!(TempLong.LANByte[3] & ECAT_CSR_BUSY))
            break;
        udelay(100); /* Use udelay instead of msleep */
        timeout--;
    } while (timeout > 0);

    if (timeout <= 0) {
        dev_err(&dev->spi->dev, "Timeout writing register 0x%04x\n", address);
    }
}

/* Read from process RAM FIFO - non-blocking version */
static void etc_read_fifo_nb(struct lan9252_data *dev)
{
    ULONG TempLong;
    u8 tx_buf[35], rx_buf[35];
    uint8_t i;
    int ret;
    int timeout = 10;

    etc_write_reg(dev, ECAT_PRAM_RD_ADDR_LEN, 0x00201000);
    etc_write_reg(dev, ECAT_PRAM_RD_CMD, 0x80000000);
    
    do {
        TempLong.LANLong = etc_read_reg(dev, ECAT_PRAM_RD_CMD, 4);
        if ((TempLong.LANByte[0] & PRAM_READ_AVAIL) && (TempLong.LANByte[1] == 8))
            break;
        udelay(100);
        timeout--;
    } while (timeout > 0);

    if (timeout <= 0) {
        dev_err(&dev->spi->dev, "Timeout reading FIFO\n");
        return;
    }

    tx_buf[0] = COMM_SPI_READ;
    tx_buf[1] = 0x00;
    tx_buf[2] = 0x00;
    
    for (i = 0; i < 32; i++) {
        tx_buf[i + 3] = DUMMY_BYTE;
    }

    mutex_lock(&dev->lock);
    ret = lan9252_spi_transfer(dev->spi, tx_buf, rx_buf, 35);
    mutex_unlock(&dev->lock);

    if (ret < 0) {
        dev_err(&dev->spi->dev, "FIFO read failed: %d\n", ret);
        return;
    }

    for (i = 0; i < 32; i++) {
        dev->buffer_out.LANByte[i] = rx_buf[i + 3];
    }
}

/* Write to process RAM FIFO - non-blocking version */
static void etc_write_fifo_nb(struct lan9252_data *dev)
{
    ULONG TempLong;
    u8 tx_buf[35], rx_buf[35];
    uint8_t i;
    int ret;
    int timeout = 10;

    etc_write_reg(dev, ECAT_PRAM_WR_ADDR_LEN, 0x00201200);
    etc_write_reg(dev, ECAT_PRAM_WR_CMD, 0x80000000);
    
    do {
        TempLong.LANLong = etc_read_reg(dev, ECAT_PRAM_WR_CMD, 4);
        if ((TempLong.LANByte[0] & PRAM_WRITE_AVAIL) && (TempLong.LANByte[1] >= 8))
            break;
        udelay(100);
        timeout--;
    } while (timeout > 0);

    if (timeout <= 0) {
        dev_err(&dev->spi->dev, "Timeout writing FIFO\n");
        return;
    }

    tx_buf[0] = COMM_SPI_WRITE;
    tx_buf[1] = 0x00;
    tx_buf[2] = 0x20;
    
    for (i = 0; i < 32; i++) {
        tx_buf[i + 3] = dev->buffer_in.LANByte[i];
    }

    mutex_lock(&dev->lock);
    ret = lan9252_spi_transfer(dev->spi, tx_buf, rx_buf, 35);
    mutex_unlock(&dev->lock);

    if (ret < 0) {
        dev_err(&dev->spi->dev, "FIFO write failed: %d\n", ret);
    }
}

/* Initialize device */
static bool etc_init(struct lan9252_data *dev)
{
    ULONG TempLong;

    etc_write_reg(dev, RESET_CTL, (DIGITAL_RST & ETHERCAT_RST));
    msleep(100);
    
    TempLong.LANLong = etc_read_reg(dev, BYTE_TEST, 4);
    dev_info(&dev->spi->dev, "BYTE_TEST register = 0x%08x\n", TempLong.LANLong);

    if (TempLong.LANLong != 0x87654321) {
        dev_err(&dev->spi->dev, "Bad response from test register: 0x%08x\n", TempLong.LANLong);
        return false;
    }

    TempLong.LANLong = etc_read_reg(dev, HW_CFG, 4);
    if ((TempLong.LANLong & READY) == 0) {
        dev_err(&dev->spi->dev, "Device not ready: 0x%08x\n", TempLong.LANLong);
        return false;
    }

    dev_info(&dev->spi->dev, "LAN9252 initialized successfully\n");
    return true;
}

/* Process one scan - non-blocking version */
static uint8_t etc_scan_nb(struct lan9252_data *dev)
{
    ULONG TempLong;
    uint8_t Status;
    uint8_t i;

    TempLong.LANLong = etc_read_reg_wait_nb(dev, WDOG_STATUS, 1);
    dev->watchdog_active = (TempLong.LANByte[0] & 0x01) ? 0 : 1;

    TempLong.LANLong = etc_read_reg_wait_nb(dev, AL_STATUS_REG_0, 1);
    Status = TempLong.LANByte[0] & 0x0F;
    dev->operational = (Status == ESM_OP) ? 1 : 0;

    if (dev->watchdog_active || !dev->operational) {
        for (i = 0; i < 8; i++) {
            dev->buffer_out.LANLong[i] = 0;
        }
    } else {
        etc_read_fifo_nb(dev);
    }

    etc_write_fifo_nb(dev);

    if (dev->watchdog_active) {
        Status |= 0x80;
    }

    dev->last_status = Status;
    
    /* Print process data to dmesg */
    printk(KERN_INFO "LAN9252: Status: 0x%02x, Op: %d, WD: %d, "
           "Out: 0x%08x 0x%08x, In: 0x%08x 0x%08x\n",
           Status, dev->operational, dev->watchdog_active,
           dev->buffer_out.LANLong[0], dev->buffer_out.LANLong[1],
           dev->buffer_in.LANLong[0], dev->buffer_in.LANLong[1]);

    return Status;
}

/* Workqueue function for scanning */
static void etc_scan_work(struct work_struct *work)
{
    struct lan9252_data *dev = container_of(work, struct lan9252_data, scan_work);
    etc_scan_nb(dev);
}

/* Timer callback for periodic scanning */
static void etc_scan_timer_callback(struct timer_list *t)
{
    struct lan9252_data *dev = from_timer(dev, t, scan_timer);
    
    /* Schedule work in workqueue context */
    schedule_work(&dev->scan_work);
    
    /* Reschedule the timer */
    mod_timer(&dev->scan_timer, jiffies + msecs_to_jiffies(SCAN_INTERVAL_MS));
}

/* Sysfs interface for process data */
static ssize_t process_data_out_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    struct lan9252_data *lan9252 = dev_get_drvdata(dev);
    ssize_t count = 0;
    int i;

    mutex_lock(&lan9252->lock);
    for (i = 0; i < 8; i++) {
        count += sprintf(buf + count, "0x%08x ", lan9252->buffer_out.LANLong[i]);
    }
    count += sprintf(buf + count, "\n");
    mutex_unlock(&lan9252->lock);

    return count;
}

static ssize_t process_data_in_store(struct device *dev, struct device_attribute *attr,
                                   const char *buf, size_t count)
{
    struct lan9252_data *lan9252 = dev_get_drvdata(dev);
    int i;
    unsigned int dword;

    mutex_lock(&lan9252->lock);
    for (i = 0; i < 8 && i < count / 11; i++) {
        if (sscanf(buf + i * 11, "0x%08x", &dword) == 1) {
            lan9252->buffer_in.LANLong[i] = dword;
        }
    }
    mutex_unlock(&lan9252->lock);

    return count;
}

static ssize_t status_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    struct lan9252_data *lan9252 = dev_get_drvdata(dev);
    
    return sprintf(buf, "0x%02x\n", lan9252->last_status);
}

static DEVICE_ATTR(process_data_out, 0444, process_data_out_show, NULL);
static DEVICE_ATTR(process_data_in, 0200, NULL, process_data_in_store);
static DEVICE_ATTR(status, 0444, status_show, NULL);

/* Probe Function */
static int lan9252_probe(struct spi_device *spi)
{
    struct lan9252_data *lan9252;
    int ret;

    lan9252 = devm_kzalloc(&spi->dev, sizeof(*lan9252), GFP_KERNEL);
    if (!lan9252)
        return -ENOMEM;

    lan9252->spi = spi;
    spi_set_drvdata(spi, lan9252);
    mutex_init(&lan9252->lock);

    /* Configure SPI */
    spi->mode = SPI_MODE_0;
    spi->bits_per_word = 8;
    ret = spi_setup(spi);
    if (ret < 0) {
        dev_err(&spi->dev, "SPI setup failed: %d\n", ret);
        return ret;
    }

    /* Initialize LAN9252 */
    if (!etc_init(lan9252)) {
        dev_err(&spi->dev, "LAN9252 initialization failed\n");
        return -ENODEV;
    }

    /* Initialize workqueue and timer for periodic scanning */
    INIT_WORK(&lan9252->scan_work, etc_scan_work);
    timer_setup(&lan9252->scan_timer, etc_scan_timer_callback, 0);
    mod_timer(&lan9252->scan_timer, jiffies + msecs_to_jiffies(SCAN_INTERVAL_MS));

    /* Create sysfs files */
    ret = device_create_file(&spi->dev, &dev_attr_process_data_out);
    if (ret < 0) {
        dev_err(&spi->dev, "Failed to create process_data_out sysfs file\n");
        goto err_timer;
    }

    ret = device_create_file(&spi->dev, &dev_attr_process_data_in);
    if (ret < 0) {
        dev_err(&spi->dev, "Failed to create process_data_in sysfs file\n");
        goto err_sysfs1;
    }

    ret = device_create_file(&spi->dev, &dev_attr_status);
    if (ret < 0) {
        dev_err(&spi->dev, "Failed to create status sysfs file\n");
        goto err_sysfs2;
    }

    dev_info(&spi->dev, "LAN9252 driver probed successfully\n");
    return 0;

err_sysfs2:
    device_remove_file(&spi->dev, &dev_attr_process_data_in);
err_sysfs1:
    device_remove_file(&spi->dev, &dev_attr_process_data_out);
err_timer:
    del_timer_sync(&lan9252->scan_timer);
    return ret;
}

/* Remove Function */
static void lan9252_remove(struct spi_device *spi)
{
    struct lan9252_data *lan9252 = spi_get_drvdata(spi);
    
    del_timer_sync(&lan9252->scan_timer);
    cancel_work_sync(&lan9252->scan_work);
    device_remove_file(&spi->dev, &dev_attr_process_data_out);
    device_remove_file(&spi->dev, &dev_attr_process_data_in);
    device_remove_file(&spi->dev, &dev_attr_status);
    dev_info(&spi->dev, "LAN9252 driver removed\n");
}

/* Device Tree Match */
static const struct of_device_id lan9252_of_match[] = {
    { .compatible = "microchip,lan9252" },
    { }
};
MODULE_DEVICE_TABLE(of, lan9252_of_match);

/* SPI Driver */
static struct spi_driver lan9252_driver = {
    .driver = {
        .name = DRIVER_NAME,
        .of_match_table = lan9252_of_match,
    },
    .probe = lan9252_probe,
    .remove = lan9252_remove,
};

module_spi_driver(lan9252_driver);

MODULE_DESCRIPTION("LAN9252 EtherCAT SPI Driver");
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");
