import sys
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QToolButton, QLabel, QRadioButton
)
from PySide6.QtGui import QCursor

from PySide6.QtCore import Qt, QTimer

from ui_home1 import Ui_MainWindow as Ui_Home1
from ui_home2 import Ui_MainWindow as Ui_Home2
from gpio import GPIOControl

# Constants for button presses as bitwise values
CYCLE_START = 1 << 0
CYCLE_STOP = 1 << 1
SERVO = 1 << 2
JOG = 1 << 3
X = 1 << 4
PLUS = 1 << 5
Z_LOCK = 1 << 6
# MDI = 1 << 7
Y = 1 << 8
ZERO = 1 << 9
DRY_RUN = 1 << 10
AUTO = 1 << 11
Z = 1 << 12
MINUS = 1 << 13
# NC_REF = 1 << 14
NC_OFFSET = 1 << 15
RET_FOR = 1 << 16
RET_REV = 1 << 17
PRC_END = 1 << 18
ALM_OVR = 1 << 19
ALM_RST = 1 << 20
CLEAN = 1 << 21
# LOCK_RST = 1 << 21
LASER_ON = 1 << 22
LASER_READY= 1<< 23

INTERVAL = 50


class Home1Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Home1()
        self.ui.setupUi(self)


class Home2Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Home2()
        self.ui.setupUi(self)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Machine Control Panel")

        self.setAttribute(Qt.WA_Hover, False)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAutoFillBackground(False)
        self.setMouseTracking(False)
        self.setCursor(QCursor(Qt.BlankCursor))
        # Frameless fullscreen
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        # Central stacked widget
        self.stacked_central = QStackedWidget()
        self.setCentralWidget(self.stacked_central)

        # Load both pages
        self.home1 = Home1Widget()
        self.home2 = Home2Widget()

        self.gpio = GPIOControl()
        # Apply JSON button renames
        self.apply_button_texts("en","buttons.json")

        # Add to stack
        self.stacked_central.addWidget(self.home1)
        self.stacked_central.addWidget(self.home2)
        self.stacked_central.setCurrentWidget(self.home1)

        # Disable hover/mouse tracking globally
        for widget in self.findChildren(QWidget):
            widget.setAttribute(Qt.WA_Hover, False)
            widget.setMouseTracking(False)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run_periodic_tasks)
        self.timer.start(INTERVAL)
        self.buttonStatus = 0

        self.init_buttons()
        self.write_process_data(self.buttonStatus)

    def apply_button_texts(self, language, json_file):
        """Load button texts from JSON and apply to both home1 and home2."""
        try:
            with open("buttons.json", "r", encoding="utf-8") as f:
                translations = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Warning: Could not load {json_file}")
            return
        lang = language 
        # Apply to both pages
        for page in (self.home1, self.home2):
            for obj_name, text in translations[lang].items():
                widget = page.findChild(QWidget, obj_name)
                if widget:
                    if isinstance(widget, (QToolButton, QLabel)):
                        widget.setText(text)


    def init_buttons(self):
        self.home1.ui.laserReadyLed.setEnabled(False)
        self.home2.ui.laserReadyLed.setEnabled(False)
        self.set_autoMode_buttons(False)
        # Navigation
        self.home1.ui.jogButton.pressed.connect(
            lambda: (self.stacked_central.setCurrentWidget(self.home2),
                    self.handle_button_pressed(JOG),
                    self.set_jogMode_buttons(False))
        )
        self.home1.ui.autoButton.pressed.connect(
            lambda: (self.stacked_central.setCurrentWidget(self.home1),
                    self.handle_button_pressed(AUTO),
                    self.set_autoMode_buttons(False))
        )
        self.home2.ui.jogButton.pressed.connect(
            lambda: (self.stacked_central.setCurrentWidget(self.home2),
                    self.handle_button_pressed(JOG),
                    self.set_jogMode_buttons(False))
        )
        self.home2.ui.autoButton.pressed.connect(
            lambda: (self.stacked_central.setCurrentWidget(self.home1),
                    self.handle_button_pressed(AUTO),
                    self.set_autoMode_buttons(False))
        )

        # Page-I pressed
        self.home1.ui.zLockButton.pressed.connect(
            lambda: self.handle_button_pressed(Z_LOCK)
        )
        self.home1.ui.offsetButton.pressed.connect(
            lambda: self.handle_button_pressed(NC_OFFSET)
        )
        self.home1.ui.prcEndButton.pressed.connect(
            lambda: self.handle_button_pressed(PRC_END)
        )
        self.home1.ui.retForButton.pressed.connect(
            lambda: self.handle_button_pressed(RET_FOR)
        )
        self.home1.ui.dryRunButton.pressed.connect(
            lambda: self.handle_button_pressed(DRY_RUN)
        )
        self.home1.ui.retRevButton.pressed.connect(
            lambda: self.handle_button_pressed(RET_REV)
        )
        self.home1.ui.cycleStartButton.pressed.connect(
            lambda: self.handle_button_pressed(CYCLE_START)
        )
        self.home1.ui.cycleStopButton.pressed.connect(
            lambda: self.handle_button_pressed(CYCLE_STOP)
        )

        # Page-II pressed
        self.home2.ui.xButton.pressed.connect(lambda: self.handle_button_pressed(X))
        self.home2.ui.yButton.pressed.connect(lambda: self.handle_button_pressed(Y))
        self.home2.ui.zButton.pressed.connect(lambda: self.handle_button_pressed(Z))
        self.home2.ui.plusButton.pressed.connect(
            lambda: self.handle_button_pressed(PLUS)
        )
        self.home2.ui.zeroButton.pressed.connect(
            lambda: self.handle_button_pressed(ZERO)
        )
        self.home2.ui.minusButton.pressed.connect(
            lambda: self.handle_button_pressed(MINUS)
        )
        self.home2.ui.cleanButton.pressed.connect(lambda: self.handle_button_pressed(CLEAN))

        # Common pressed
        self.home1.ui.servoEnableButton.pressed.connect(
            lambda: self.handle_button_pressed(SERVO)
        )
        self.home1.ui.almOvrButton.pressed.connect(
            lambda: self.handle_button_pressed(ALM_OVR)
        )
        self.home1.ui.almRstButton.pressed.connect(
            lambda: self.handle_button_pressed(ALM_RST)
        )
        self.home1.ui.laserOnButton.toggled.connect(
            lambda checked: self.on_laserOnButton_toggled(checked)
        )
        self.home1.ui.lanEngBtn.toggled.connect(
            lambda checked: self.lanEngbtn_toggled(checked)
        )

        self.home2.ui.servoEnableButton.pressed.connect(
            lambda: self.handle_button_pressed(SERVO)
        )
        self.home2.ui.almOvrButton.pressed.connect(
            lambda: self.handle_button_pressed(ALM_OVR)
        )
        self.home2.ui.almRstButton.pressed.connect(
            lambda: self.handle_button_pressed(ALM_RST)
        )
        self.home2.ui.laserOnButton.toggled.connect(
            lambda checked: self.on_laserOnButton_toggled(checked)
        )
        self.home2.ui.lanEngBtn.toggled.connect(
            lambda checked: self.lanEngbtn_toggled(checked)
        )
        self.home1.ui.autoButton.released.connect(lambda: self.handle_button_released(AUTO))
        self.home1.ui.jogButton.released.connect(lambda: self.handle_button_released(JOG))
        self.home2.ui.autoButton.released.connect(lambda: self.handle_button_released(AUTO))
        self.home2.ui.jogButton.released.connect(lambda: self.handle_button_released(JOG))


        # Page-I released
        self.home1.ui.zLockButton.released.connect(
            lambda: self.handle_button_released(Z_LOCK)
        )
        self.home1.ui.offsetButton.released.connect(
            lambda: self.handle_button_released(NC_OFFSET)
        )
        self.home1.ui.prcEndButton.released.connect(
            lambda: self.handle_button_released(PRC_END)
        )
        self.home1.ui.retForButton.released.connect(
            lambda: self.handle_button_released(RET_FOR)
        )
        self.home1.ui.dryRunButton.released.connect(
            lambda: self.handle_button_released(DRY_RUN)
        )
        self.home1.ui.retRevButton.released.connect(
            lambda: self.handle_button_released(RET_REV)
        )
        self.home1.ui.cycleStartButton.released.connect(
            lambda: self.handle_button_released(CYCLE_START)
        )
        self.home1.ui.cycleStopButton.released.connect(
            lambda: self.handle_button_released(CYCLE_STOP)
        )

        # Page-II released
        self.home2.ui.xButton.released.connect(lambda: self.handle_button_released(X))
        self.home2.ui.yButton.released.connect(lambda: self.handle_button_released(Y))
        self.home2.ui.zButton.released.connect(lambda: self.handle_button_released(Z))
        self.home2.ui.plusButton.released.connect(
            lambda: self.handle_button_released(PLUS)
        )
        self.home2.ui.zeroButton.released.connect(
            lambda: self.handle_button_released(ZERO)
        )
        self.home2.ui.minusButton.released.connect(
            lambda: self.handle_button_released(MINUS)
        )
        self.home2.ui.cleanButton.released.connect(lambda: self.handle_button_released(CLEAN))

        # Common released
        self.home1.ui.servoEnableButton.released.connect(
            lambda: self.handle_button_released(SERVO)
        )
        self.home1.ui.almOvrButton.released.connect(
            lambda: self.handle_button_released(ALM_OVR)
        )
        self.home1.ui.almRstButton.released.connect(
            lambda: self.handle_button_released(ALM_RST)
        )

        self.home2.ui.servoEnableButton.released.connect(
            lambda: self.handle_button_released(SERVO)
        )
        self.home2.ui.almOvrButton.released.connect(
            lambda: self.handle_button_released(ALM_OVR)
        )
        self.home2.ui.almRstButton.released.connect(
            lambda: self.handle_button_released(ALM_RST)
        )

    def update_button_states(self, EtcInValue):
        if EtcInValue & AUTO:
            self.set_autoMode_buttons(True)
            self.set_jogMode_buttons(False)
            # self.stacked_central.setCurrentWidget(self.home1)
        elif EtcInValue & JOG:
            self.set_jogMode_buttons(True)
            self.set_autoMode_buttons(False)
            # self.stacked_central.setCurrentWidget(self.home2)
        #Page-I Buttons
        if EtcInValue & CYCLE_START:
            self.home1.ui.cycleStartButton.setChecked(True)
        else:
            self.home1.ui.cycleStartButton.setChecked(False)
        if EtcInValue & CYCLE_STOP:
            self.home1.ui.cycleStopButton.setChecked(True)
        else:
            self.home1.ui.cycleStopButton.setChecked(False)
        if EtcInValue & Z_LOCK:
            self.home1.ui.zLockButton.setChecked(True)
        else:
            self.home1.ui.zLockButton.setChecked(False)
        if EtcInValue & NC_OFFSET:
            self.home1.ui.offsetButton.setChecked(True)
        else:
            self.home1.ui.offsetButton.setChecked(False)
        if EtcInValue & PRC_END:
            self.home1.ui.prcEndButton.setChecked(True)
        else:
            self.home1.ui.prcEndButton.setChecked(False)
        if EtcInValue & RET_FOR:
            self.home1.ui.retForButton.setChecked(True)
        else:
            self.home1.ui.retForButton.setChecked(False)
        if EtcInValue & DRY_RUN:    
            self.home1.ui.dryRunButton.setChecked(True)
        else:
            self.home1.ui.dryRunButton.setChecked(False)
        if EtcInValue & RET_REV:
            self.home1.ui.retRevButton.setChecked(True)
        else:
            self.home1.ui.retRevButton.setChecked(False)

        # Page-II Buttons
        if EtcInValue & X:
            self.home2.ui.xButton.setChecked(True)
        else:
            self.home2.ui.xButton.setChecked(False)
        if EtcInValue & Y:
            self.home2.ui.yButton.setChecked(True)
        else:
            self.home2.ui.yButton.setChecked(False)
        if EtcInValue & Z:
            self.home2.ui.zButton.setChecked(True)
        else:
            self.home2.ui.zButton.setChecked(False)
        if EtcInValue & PLUS:
            self.home2.ui.plusButton.setChecked(True)
        else:
            self.home2.ui.plusButton.setChecked(False)
        if EtcInValue & ZERO:
            self.home2.ui.zeroButton.setChecked(True)
        else:
            self.home2.ui.zeroButton.setChecked(False)
        if EtcInValue & MINUS:
            self.home2.ui.minusButton.setChecked(True)
        else:
            self.home2.ui.minusButton.setChecked(False)
        if EtcInValue & CLEAN:
            self.home2.ui.cleanButton.setChecked(True)
        else:
            self.home2.ui.cleanButton.setChecked(False)

        #common Buttons
        if EtcInValue & LASER_READY:
            self.home1.ui.laserReadyLed.setChecked(True)
            self.home2.ui.laserReadyLed.setChecked(True)
        else:
            self.home1.ui.laserReadyLed.setChecked(False)
            self.home2.ui.laserReadyLed.setChecked(False)
        if EtcInValue & SERVO:
            self.home1.ui.servoEnableButton.setChecked(True)
            self.home2.ui.servoEnableButton.setChecked(True)
        else:
            self.home1.ui.servoEnableButton.setChecked(False)
            self.home2.ui.servoEnableButton.setChecked(False)
        if EtcInValue & ALM_OVR:
            self.home1.ui.almOvrButton.setChecked(True)
            self.home2.ui.almOvrButton.setChecked(True)
        else:
            self.home1.ui.almOvrButton.setChecked(False)
            self.home2.ui.almOvrButton.setChecked(False)
        if EtcInValue & ALM_RST:
            self.home1.ui.almRstButton.setChecked(True)
            self.home2.ui.almRstButton.setChecked(True)
        else:
            self.home1.ui.almRstButton.setChecked(False)
            self.home2.ui.almRstButton.setChecked(False)
        

#------------------------Functions for Button Events------------------------#
    def run_periodic_tasks(self):
        # Read the first value from process_data_out
        EtcInValue = self.read_process_data_first()
        self.update_button_states(EtcInValue)
        self.gpioOutputValue = (EtcInValue >> 24) & 0xFF
        self.gpio.gpioSet(self.gpioOutputValue)
        self.gpioInValue = self.gpio.gpioGet()
        self.write_process_data(self.buttonStatus | ((self.gpioInValue & 0xFF) << 24))


    def handle_button_pressed(self, button_value):
        self.buttonStatus |= button_value
        self.write_process_data(self.buttonStatus)

    def handle_button_released(self, button_value):
        self.buttonStatus &= ~button_value
        self.write_process_data(self.buttonStatus)

    def on_laserOnButton_toggled(self, checked):
        if checked:
            self.home1.ui.laserOnButton.setChecked(True)
            self.home2.ui.laserOnButton.setChecked(True)
            self.buttonStatus |= LASER_ON

        else:
            self.buttonStatus &= ~LASER_ON
            self.home1.ui.laserOnButton.setChecked(False)
            self.home2.ui.laserOnButton.setChecked(False)
        self.write_process_data(self.buttonStatus)

    def lanEngbtn_toggled(self, checked):
        if checked:
            self.apply_button_texts("en", "buttons.json")
            self.home1.ui.lanEngBtn.setChecked(True)
            self.home2.ui.lanEngBtn.setChecked(True)
        else:
            self.apply_button_texts("ja", "buttons.json")
            self.home1.ui.lanJapBtn.setChecked(True)
            self.home2.ui.lanJapBtn.setChecked(True)

    def write_process_data(self, value, path="/sys/bus/spi/devices/spi0.0/process_data_in"):
        # Create a string with the first value as the input, others as 0x00000000
        data = f"0x{value:08X} 0x00000000 0x00000000 0x00000000 0x00000000 0x00000000 0x00000000 0x00000000"
        with open(path, "w") as f:
            f.write(data)  # Add newline to ensure proper write

    def read_process_data_first(self, path="/sys/bus/spi/devices/spi0.0/process_data_out"):
        with open(path, "r") as f:
            content = f.read().strip()
        first_hex = content.split()[0]         
        value = int(first_hex, 16)             
        return value
    def set_autoMode_buttons(self, state: bool):
        self.home1.ui.zLockButton.setEnabled(state)
        self.home1.ui.offsetButton.setEnabled(state)
        self.home1.ui.prcEndButton.setEnabled(state)
        self.home1.ui.retForButton.setEnabled(state)
        self.home1.ui.dryRunButton.setEnabled(state)
        self.home1.ui.retRevButton.setEnabled(state)
        self.home1.ui.cycleStartButton.setEnabled(state)
        self.home1.ui.cycleStopButton.setEnabled(state)

    def set_jogMode_buttons(self, state: bool):
        self.home2.ui.xButton.setEnabled(state)
        self.home2.ui.yButton.setEnabled(state)
        self.home2.ui.zButton.setEnabled(state)
        self.home2.ui.plusButton.setEnabled(state)
        self.home2.ui.zeroButton.setEnabled(state)
        self.home2.ui.minusButton.setEnabled(state)
        self.home2.ui.cleanButton.setEnabled(state)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.gpio.gpio_release()
            QApplication.quit()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
