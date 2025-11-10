#include <linux/module.h>
#include <linux/export-internal.h>
#include <linux/compiler.h>

MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};



static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0xafbeba1c, "__spi_register_driver" },
	{ 0x3c3ff9fd, "sprintf" },
	{ 0x4dfa8d4b, "mutex_lock" },
	{ 0xbcab6ee6, "sscanf" },
	{ 0x3213f038, "mutex_unlock" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0x82ee90dc, "timer_delete_sync" },
	{ 0x3c12dfe, "cancel_work_sync" },
	{ 0xca192dd7, "device_remove_file" },
	{ 0x1a283f39, "_dev_info" },
	{ 0xdcb764ad, "memset" },
	{ 0x9c771906, "spi_sync" },
	{ 0xf810f451, "_dev_err" },
	{ 0x4829a47e, "memcpy" },
	{ 0xfa61d21, "devm_kmalloc" },
	{ 0xcefb0c9f, "__mutex_init" },
	{ 0x41e0584a, "spi_setup" },
	{ 0xf9a482f9, "msleep" },
	{ 0xc6f46339, "init_timer_key" },
	{ 0x15ba50a6, "jiffies" },
	{ 0xc38c83b8, "mod_timer" },
	{ 0x89c41bdf, "device_create_file" },
	{ 0xd51bf3d7, "driver_unregister" },
	{ 0xeae3dfd6, "__const_udelay" },
	{ 0x122c3a7e, "_printk" },
	{ 0x2d3385d3, "system_wq" },
	{ 0xc5b6f236, "queue_work_on" },
	{ 0x39ff040a, "module_layout" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("of:N*T*Cmicrochip,lan9252");
MODULE_ALIAS("of:N*T*Cmicrochip,lan9252C*");

MODULE_INFO(srcversion, "D25A5BD36930E7FB564E1A5");
