import sys
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QToolButton, QLabel, QRadioButton
)
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt
from ctypes import c_uint32
import time
import threading
#import files
from ui_home1 import Ui_MainWindow as Ui_Home1
from ui_home2 import Ui_MainWindow as Ui_Home2
from Ethercat import EtherCATInterface
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

INTERVAL = 0.200   #Thread interval in seconds

etc_out = c_uint32(0)

#-----------------------------------Ethercat Thread-----------------------------------
class EtherCATThread(QThread):
    # Define a signal to send the etc_out value to the main thread
    data_ready = QtCore.pyqtSignal(int)
    gpio_data = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.etc_interface = EtherCATInterface()
        self.etc_init_ok = False
        self.shared_lock = threading.Lock()  # Lock for thread-safe updates
        self.gpio_ctrl = GPIOControl()

    def run(self):       
        self.etc_init_ok = self.etc_interface.etc_init()
        EtcOutValue = 0
        pre_EtcOutValue = 0
        EtcOut_gpioValue = 0
        pre_EtcOut_gpioValue = 0
        while True:
            if self.etc_init_ok:
                with self.shared_lock:
                    gpio_value = (self.gpio_ctrl.gpio_input_scan() & 0xFF) << 24
                    button_value = self.etc_interface.Etc_Buffer_In.LANLong[0] & 0x00FFFFFF
                    self.etc_interface.Etc_Buffer_In.LANLong[0] =  button_value | gpio_value
                    self.etc_interface.etc_scan()
                    EtcOutValue = self.etc_interface.Etc_Buffer_Out.LANLong[0]
                    EtcOut_gpioValue = (self.etc_interface.Etc_Buffer_Out.LANLong[0] >> 24) & 0xFF
                if EtcOutValue != pre_EtcOutValue:
                    self.data_ready.emit(EtcOutValue)
                if EtcOut_gpioValue != pre_EtcOut_gpioValue:
                    self.gpio_data.emit(EtcOut_gpioValue)
            else:
                self.etc_init_ok = self.etc_interface.etc_init()               
            pre_EtcOutValue = EtcOutValue
            pre_EtcOut_gpioValue = EtcOut_gpioValue
            time.sleep(INTERVAL)

#-----------------------------------Main Window-----------------------------------
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

        self.buttonStatus = 0

        self.ethercatThread = EtherCATThread()
        self.shared_lock = threading.Lock()
        self.etc_interface = EtherCATInterface()
        self.gpio_ctrl = GPIOControl()
        
        self.ethercatThread.data_ready.connect(self.update_ui)
        self.ethercatThread.gpio_data.connect(self.gpio_ctrl.gpio_output_control)
        self.ethercatThread.start()

        self.init_buttons()
        

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

    def update_ui(self, EtcOutValue):
        if EtcOutValue & AUTO:
            self.set_autoMode_buttons(True)
            self.set_jogMode_buttons(False)
            # self.stacked_central.setCurrentWidget(self.home1)
        elif EtcOutValue & JOG:
            self.set_jogMode_buttons(True)
            self.set_autoMode_buttons(False)
            # self.stacked_central.setCurrentWidget(self.home2)
        #Page-I Buttons
        if EtcOutValue & CYCLE_START:
            self.home1.ui.cycleStartButton.setChecked(True)
        else:
            self.home1.ui.cycleStartButton.setChecked(False)
        if EtcOutValue & CYCLE_STOP:
            self.home1.ui.cycleStopButton.setChecked(True)
        else:
            self.home1.ui.cycleStopButton.setChecked(False)
        if EtcOutValue & Z_LOCK:
            self.home1.ui.zLockButton.setChecked(True)
        else:
            self.home1.ui.zLockButton.setChecked(False)
        if EtcOutValue & NC_OFFSET:
            self.home1.ui.offsetButton.setChecked(True)
        else:
            self.home1.ui.offsetButton.setChecked(False)
        if EtcOutValue & PRC_END:
            self.home1.ui.prcEndButton.setChecked(True)
        else:
            self.home1.ui.prcEndButton.setChecked(False)
        if EtcOutValue & RET_FOR:
            self.home1.ui.retForButton.setChecked(True)
        else:
            self.home1.ui.retForButton.setChecked(False)
        if EtcOutValue & DRY_RUN:    
            self.home1.ui.dryRunButton.setChecked(True)
        else:
            self.home1.ui.dryRunButton.setChecked(False)
        if EtcOutValue & RET_REV:
            self.home1.ui.retRevButton.setChecked(True)
        else:
            self.home1.ui.retRevButton.setChecked(False)

        # Page-II Buttons
        if EtcOutValue & X:
            self.home2.ui.xButton.setChecked(True)
        else:
            self.home2.ui.xButton.setChecked(False)
        if EtcOutValue & Y:
            self.home2.ui.yButton.setChecked(True)
        else:
            self.home2.ui.yButton.setChecked(False)
        if EtcOutValue & Z:
            self.home2.ui.zButton.setChecked(True)
        else:
            self.home2.ui.zButton.setChecked(False)
        if EtcOutValue & PLUS:
            self.home2.ui.plusButton.setChecked(True)
        else:
            self.home2.ui.plusButton.setChecked(False)
        if EtcOutValue & ZERO:
            self.home2.ui.zeroButton.setChecked(True)
        else:
            self.home2.ui.zeroButton.setChecked(False)
        if EtcOutValue & MINUS:
            self.home2.ui.minusButton.setChecked(True)
        else:
            self.home2.ui.minusButton.setChecked(False)
        if EtcOutValue & CLEAN:
            self.home2.ui.cleanButton.setChecked(True)
        else:
            self.home2.ui.cleanButton.setChecked(False)

        #common Buttons
        if EtcOutValue & LASER_READY:
            self.home1.ui.laserReadyLed.setChecked(True)
            self.home2.ui.laserReadyLed.setChecked(True)
        else:
            self.home1.ui.laserReadyLed.setChecked(False)
            self.home2.ui.laserReadyLed.setChecked(False)
        if EtcOutValue & SERVO:
            self.home1.ui.servoEnableButton.setChecked(True)
            self.home2.ui.servoEnableButton.setChecked(True)
        else:
            self.home1.ui.servoEnableButton.setChecked(False)
            self.home2.ui.servoEnableButton.setChecked(False)
        if EtcOutValue & ALM_OVR:
            self.home1.ui.almOvrButton.setChecked(True)
            self.home2.ui.almOvrButton.setChecked(True)
        else:
            self.home1.ui.almOvrButton.setChecked(False)
            self.home2.ui.almOvrButton.setChecked(False)
        if EtcOutValue & ALM_RST:
            self.home1.ui.almRstButton.setChecked(True)
            self.home2.ui.almRstButton.setChecked(True)
        else:
            self.home1.ui.almRstButton.setChecked(False)
            self.home2.ui.almRstButton.setChecked(False)
        

#------------------------Functions for Button Events------------------------#
    def handle_button_pressed(self, button_value):
        self.buttonStatus |= button_value
        with self.shared_lock:
            self.ethercatThread.etc_interface.Etc_Buffer_In.LANLong[0] |= self.buttonStatus

    def handle_button_released(self, button_value):
        self.buttonStatus &= ~button_value
        with self.shared_lock:
            self.ethercatThread.etc_interface.Etc_Buffer_In.LANLong[0] &= ~self.buttonStatus

    def on_laserOnButton_toggled(self, checked):
        if checked:
            self.home1.ui.laserOnButton.setChecked(True)
            self.home2.ui.laserOnButton.setChecked(True)
            self.buttonStatus |= LASER_ON
        else:
            self.buttonStatus &= ~LASER_ON
            self.home1.ui.laserOnButton.setChecked(False)
            self.home2.ui.laserOnButton.setChecked(False)
        with self.shared_lock:
            self.ethercatThread.etc_interface.Etc_Buffer_In.LANLong[0] = self.buttonStatus

    def lanEngbtn_toggled(self, checked):
        if checked:
            self.apply_button_texts("en", "buttons.json")
            self.home1.ui.lanEngBtn.setChecked(True)
            self.home2.ui.lanEngBtn.setChecked(True)
        else:
            self.apply_button_texts("ja", "buttons.json")
            self.home1.ui.lanJapBtn.setChecked(True)
            self.home2.ui.lanJapBtn.setChecked(True)

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
            self.closeEvent(event)
            QApplication.quit()
        else:
            super().keyPressEvent(event)
            
    def closeEvent(self, event):
        self.gpio.gpio_release()
        self.ethercat.running = False
        self.ethercatThread.quit()
        self.ethercatThread.wait()
        self.gpio_ctrl.gpio_release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
