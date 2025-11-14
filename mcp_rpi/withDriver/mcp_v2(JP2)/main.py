import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QToolButton, QLabel, QDialog,
    QVBoxLayout, QLineEdit, QGridLayout, QPushButton, QComboBox, QMessageBox, QHBoxLayout, QFileDialog
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap, QImage, QPainter, QCursor
from PySide6.QtSvg import QSvgRenderer

from ui_home1 import Ui_MainWindow as Ui_Home1
from ui_home2 import Ui_MainWindow as Ui_Home2
from settings import PasswordDialog, SettingsDialog
from gpio import GPIOControl

# Constants for button presses as bitwise values
CYCLE_START = 1 << 0
CYCLE_STOP = 1 << 1
SERVO = 1 << 2
JOG = 1 << 3
X = 1 << 4
PLUS = 1 << 5
Z_LOCK = 1 << 6
PANEL_UP = 1 << 7
Y = 1 << 8
ZERO = 1 << 9
DRY_RUN = 1 << 10
AUTO = 1 << 11
Z = 1 << 12
MINUS = 1 << 13
PANEL_DOWN = 1 << 14
NC_OFFSET = 1 << 15
RET_FOR = 1 << 16
RET_REV = 1 << 17
PRC_END = 1 << 18
ALM_OVR = 1 << 19
ALM_RST = 1 << 20
DOOR_UNLOCK = 1 << 21
LASER_ON = 1 << 22
LASER_READY= 1<< 23
#24-31 reserved for GPIOs
NOZZLE_CHANGE = 1 << 32
#communication interval in ms
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
        self.in_path="/sys/bus/spi/devices/spi0.0/process_data_in"
        self.out_path="/sys/bus/spi/devices/spi0.0/process_data_out"
        self.in_file = open(self.in_path, "w")
        self.out_file = open(self.out_path, "r")
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
        self.autoPanel = Home1Widget()
        self.jogPanel = Home2Widget()

        self.gpio = GPIOControl()

        # Add to stack
        self.stacked_central.addWidget(self.autoPanel)
        self.stacked_central.addWidget(self.jogPanel)
        self.stacked_central.setCurrentWidget(self.jogPanel)

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
        self.apply_settings()

    def apply_settings(self):
        config_file = "settings.json"
        default_language = "English"
        default_logo_path = ""
        default_x = -60
        default_y = 10
        default_width = 650
        default_height = 450
        language = default_language
        logo_path = default_logo_path
        x = default_x
        y = default_y
        width = default_width
        height = default_height
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    language = config.get("language", default_language)
                    logo_path = config.get("logo_path", default_logo_path)
                    x = config.get("logo_x", default_x)
                    y = config.get("logo_y", default_y)
                    width = config.get("logo_width", default_width)
                    height = config.get("logo_height", default_height)
            except (json.JSONDecodeError, KeyError):
                pass
        self.apply_translations(language)
        self.set_logo(logo_path, x, y, width, height)

    def apply_translations(self, language):
        try:
            with open("buttons.json", "r", encoding="utf-8") as f:
                translations = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading buttons.json: {e}")
            translations = {"English": {}, "Japanese": {}}
            QMessageBox.warning(self, "Error", "Failed to load button translations. Using default texts.")
            return
        lang = language if language in translations else "English"
        # print(f"Applying language: {lang}")
        for page in (self.autoPanel, self.jogPanel):
            for obj_name, text in translations.get(lang, {}).items():
                widget = page.findChild(QWidget, obj_name)
                if widget and isinstance(widget, (QToolButton, QLabel)):
                    widget.setText(text)

    def set_logo(self, path, x, y, width, height):
        if width < 50 or height < 50:
            return  # Prevent invalid sizes
        if path and os.path.exists(path):
            if path.lower().endswith('.svg'):
                # Render SVG to QPixmap
                renderer = QSvgRenderer(path)
                if not renderer.isValid():
                    print(f"Invalid SVG file: {path}")
                    return
                image = QImage(width, height, QImage.Format_ARGB32)
                image.fill(Qt.transparent)
                painter = QPainter(image)
                renderer.render(painter)
                painter.end()
                pixmap = QPixmap.fromImage(image)
            else:
                # Handle raster images (PNG, JPG, etc.)
                pixmap = QPixmap(path)
                pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.FastTransformation)
            # Update logoLable for Home1Widget
            if hasattr(self.autoPanel.ui, 'logoLable') and isinstance(self.autoPanel.ui.logoLable, QLabel):
                self.autoPanel.ui.logoLable.setPixmap(pixmap)
                self.autoPanel.ui.logoLable.setGeometry(x, y, width, height)
            # Update logoLable for Home2Widget if it exists
            if hasattr(self.jogPanel.ui, 'logoLable') and isinstance(self.jogPanel.ui.logoLable, QLabel):
                self.jogPanel.ui.logoLable.setPixmap(pixmap)
                self.jogPanel.ui.logoLable.setGeometry(x, y, width, height)
        else:
            # Apply geometry even if no logo is set
            if hasattr(self.autoPanel.ui, 'logoLable') and isinstance(self.autoPanel.ui.logoLable, QLabel):
                self.autoPanel.ui.logoLable.setGeometry(x, y, width, height)
            if hasattr(self.jogPanel.ui, 'logoLable') and isinstance(self.jogPanel.ui.logoLable, QLabel):
                self.jogPanel.ui.logoLable.setGeometry(x, y, width, height)

    def open_password_dialog(self):
        password_dialog = PasswordDialog(self)
        if password_dialog.exec() == QDialog.Accepted:
            self.open_settings()

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.settings_saved.connect(self.apply_settings)
        dialog.exec()

    def init_buttons(self):
        self.autoPanel.ui.laserReadyLed.setEnabled(False)
        self.jogPanel.ui.laserReadyLed.setEnabled(False)
        # Navigation
        self.autoPanel.ui.jogButton.pressed.connect(
            lambda: (self.handle_button_pressed(JOG)
                    # self.stacked_central.setCurrentWidget(self.jogPanel),
                    )
        )
        self.autoPanel.ui.autoButton.pressed.connect(
            lambda: (self.handle_button_pressed(AUTO))         
        )
        self.jogPanel.ui.jogButton.pressed.connect(
            lambda: (self.handle_button_pressed(JOG))
        )
        self.jogPanel.ui.autoButton.pressed.connect(
            lambda: (self.handle_button_pressed(AUTO)
                    # self.stacked_central.setCurrentWidget(self.autoPanel),
                    )
        )

        # Page-I pressed
        self.autoPanel.ui.zLockButton.pressed.connect(
            lambda: self.handle_button_pressed(Z_LOCK)
        )
        self.autoPanel.ui.offsetButton.pressed.connect(
            lambda: self.handle_button_pressed(NC_OFFSET)
        )
        self.autoPanel.ui.prcEndButton.pressed.connect(
            lambda: self.handle_button_pressed(PRC_END)
        )
        self.autoPanel.ui.retForButton.pressed.connect(
            lambda: self.handle_button_pressed(RET_FOR)
        )
        self.autoPanel.ui.dryRunButton.pressed.connect(
            lambda: self.handle_button_pressed(DRY_RUN)
        )
        self.autoPanel.ui.retRevButton.pressed.connect(
            lambda: self.handle_button_pressed(RET_REV)
        )
        self.autoPanel.ui.cycleStartButton.pressed.connect(
            lambda: self.handle_button_pressed(CYCLE_START)
        )
        self.autoPanel.ui.cycleStopButton.pressed.connect(
            lambda: self.handle_button_pressed(CYCLE_STOP)
        )
        
        # Page-II pressed
        self.jogPanel.ui.xButton.pressed.connect(lambda: self.handle_button_pressed(X))
        self.jogPanel.ui.yButton.pressed.connect(lambda: self.handle_button_pressed(Y))
        self.jogPanel.ui.zButton.pressed.connect(lambda: self.handle_button_pressed(Z))
        self.jogPanel.ui.plusButton.pressed.connect(
            lambda: self.handle_button_pressed(PLUS)
        )
        self.jogPanel.ui.zeroButton.pressed.connect(
            lambda: self.handle_button_pressed(ZERO)
        )
        self.jogPanel.ui.minusButton.pressed.connect(
            lambda: self.handle_button_pressed(MINUS)
        )
        self.jogPanel.ui.doorUnlockButton.pressed.connect(lambda: self.handle_button_pressed(DOOR_UNLOCK))
        self.jogPanel.ui.nozzleChangeButton.toggled.connect(
            lambda checked: self.on_nozzleChangeButton_toggled(checked)
        )

        # Common pressed
        self.autoPanel.ui.servoEnableButton.pressed.connect(
            lambda: self.handle_button_pressed(SERVO)
        )
        self.autoPanel.ui.almOvrButton.pressed.connect(
            lambda: self.handle_button_pressed(ALM_OVR)
        )
        self.autoPanel.ui.almRstButton.pressed.connect(
            lambda: self.handle_button_pressed(ALM_RST)
        )
        self.autoPanel.ui.laserOnButton.toggled.connect(
            lambda checked: self.on_laserOnButton_toggled(checked)
        )
        self.autoPanel.ui.settingButton.clicked.connect(self.open_password_dialog)
        self.autoPanel.ui.panelDownButton.pressed.connect(
            lambda: self.handle_button_pressed(PANEL_DOWN)
        )
        self.autoPanel.ui.panelUpButton.pressed.connect(
            lambda: self.handle_button_pressed(PANEL_UP)
        )
        

        self.jogPanel.ui.settingButton.clicked.connect(self.open_password_dialog)
        self.jogPanel.ui.servoEnableButton.pressed.connect(
            lambda: self.handle_button_pressed(SERVO)
        )
        self.jogPanel.ui.almOvrButton.pressed.connect(
            lambda: self.handle_button_pressed(ALM_OVR)
        )
        self.jogPanel.ui.almRstButton.pressed.connect(
            lambda: self.handle_button_pressed(ALM_RST)
        )
        self.jogPanel.ui.laserOnButton.toggled.connect(
            lambda checked: self.on_laserOnButton_toggled(checked)
        )
        self.jogPanel.ui.panelDownButton.pressed.connect(
            lambda: self.handle_button_pressed(PANEL_DOWN)
        )
        self.jogPanel.ui.panelUpButton.pressed.connect(
            lambda: self.handle_button_pressed(PANEL_UP)
        )
       
        # Page-I released
        self.autoPanel.ui.zLockButton.released.connect(
            lambda: self.handle_button_released(Z_LOCK)
        )
        self.autoPanel.ui.offsetButton.released.connect(
            lambda: self.handle_button_released(NC_OFFSET)
        )
        self.autoPanel.ui.prcEndButton.released.connect(
            lambda: self.handle_button_released(PRC_END)
        )
        self.autoPanel.ui.retForButton.released.connect(
            lambda: self.handle_button_released(RET_FOR)
        )
        self.autoPanel.ui.dryRunButton.released.connect(
            lambda: self.handle_button_released(DRY_RUN)
        )
        self.autoPanel.ui.retRevButton.released.connect(
            lambda: self.handle_button_released(RET_REV)
        )
        self.autoPanel.ui.cycleStartButton.released.connect(
            lambda: self.handle_button_released(CYCLE_START)
        )
        self.autoPanel.ui.cycleStopButton.released.connect(
            lambda: self.handle_button_released(CYCLE_STOP)
        )

        # Page-II released
        self.jogPanel.ui.xButton.released.connect(lambda: self.handle_button_released(X))
        self.jogPanel.ui.yButton.released.connect(lambda: self.handle_button_released(Y))
        self.jogPanel.ui.zButton.released.connect(lambda: self.handle_button_released(Z))
        self.jogPanel.ui.plusButton.released.connect(
            lambda: self.handle_button_released(PLUS)
        )
        self.jogPanel.ui.zeroButton.released.connect(
            lambda: self.handle_button_released(ZERO)
        )
        self.jogPanel.ui.minusButton.released.connect(
            lambda: self.handle_button_released(MINUS)
        )
        self.jogPanel.ui.doorUnlockButton.released.connect(lambda: self.handle_button_released(DOOR_UNLOCK))

        # Common released
        self.autoPanel.ui.servoEnableButton.released.connect(
            lambda: self.handle_button_released(SERVO)
        )
        self.autoPanel.ui.almOvrButton.released.connect(
            lambda: self.handle_button_released(ALM_OVR)
        )
        self.autoPanel.ui.almRstButton.released.connect(
            lambda: self.handle_button_released(ALM_RST)
        )

        self.jogPanel.ui.servoEnableButton.released.connect(
            lambda: self.handle_button_released(SERVO)
        )
        self.jogPanel.ui.almOvrButton.released.connect(
            lambda: self.handle_button_released(ALM_OVR)
        )
        self.jogPanel.ui.almRstButton.released.connect(
            lambda: self.handle_button_released(ALM_RST)
        )
        self.autoPanel.ui.panelDownButton.released.connect(
            lambda: self.handle_button_released(PANEL_DOWN)
        )
        self.autoPanel.ui.panelUpButton.released.connect(
            lambda: self.handle_button_released(PANEL_UP)
        )
        self.jogPanel.ui.panelDownButton.released.connect(
            lambda: self.handle_button_released(PANEL_DOWN)
        )
        self.jogPanel.ui.panelUpButton.released.connect(
            lambda: self.handle_button_released(PANEL_UP)
        )



        self.autoPanel.ui.autoButton.released.connect(lambda: self.handle_button_released(AUTO))
        self.autoPanel.ui.jogButton.released.connect(lambda: self.handle_button_released(JOG))
        self.jogPanel.ui.autoButton.released.connect(lambda: self.handle_button_released(AUTO))
        self.jogPanel.ui.jogButton.released.connect(lambda: self.handle_button_released(JOG))

    def update_button_states(self, EtcInValue):

        if EtcInValue & JOG:
            self.stacked_central.setCurrentWidget(self.jogPanel)
        elif EtcInValue & AUTO:
            self.stacked_central.setCurrentWidget(self.autoPanel)
        #Page-I Buttons
        if EtcInValue & CYCLE_START:
            self.autoPanel.ui.cycleStartButton.setChecked(True)
        else:
            self.autoPanel.ui.cycleStartButton.setChecked(False)
        if EtcInValue & CYCLE_STOP:
            self.autoPanel.ui.cycleStopButton.setChecked(True)
        else:
            self.autoPanel.ui.cycleStopButton.setChecked(False)
        if EtcInValue & Z_LOCK:
            self.autoPanel.ui.zLockButton.setChecked(True)
        else:
            self.autoPanel.ui.zLockButton.setChecked(False)
        if EtcInValue & NC_OFFSET:
            self.autoPanel.ui.offsetButton.setChecked(True)
        else:
            self.autoPanel.ui.offsetButton.setChecked(False)
        if EtcInValue & PRC_END:
            self.autoPanel.ui.prcEndButton.setChecked(True)
        else:
            self.autoPanel.ui.prcEndButton.setChecked(False)
        if EtcInValue & RET_FOR:
            self.autoPanel.ui.retForButton.setChecked(True)
        else:
            self.autoPanel.ui.retForButton.setChecked(False)
        if EtcInValue & DRY_RUN:    
            self.autoPanel.ui.dryRunButton.setChecked(True)
        else:
            self.autoPanel.ui.dryRunButton.setChecked(False)
        if EtcInValue & RET_REV:
            self.autoPanel.ui.retRevButton.setChecked(True)
        else:
            self.autoPanel.ui.retRevButton.setChecked(False)

        # Page-II Buttons
        if EtcInValue & X:
            self.jogPanel.ui.xButton.setChecked(True)
        else:
            self.jogPanel.ui.xButton.setChecked(False)
        if EtcInValue & Y:
            self.jogPanel.ui.yButton.setChecked(True)
        else:
            self.jogPanel.ui.yButton.setChecked(False)
        if EtcInValue & Z:
            self.jogPanel.ui.zButton.setChecked(True)
        else:
            self.jogPanel.ui.zButton.setChecked(False)
        if EtcInValue & PLUS:
            self.jogPanel.ui.plusButton.setChecked(True)
        else:
            self.jogPanel.ui.plusButton.setChecked(False)
        if EtcInValue & ZERO:
            self.jogPanel.ui.zeroButton.setChecked(True)
        else:
            self.jogPanel.ui.zeroButton.setChecked(False)
        if EtcInValue & MINUS:
            self.jogPanel.ui.minusButton.setChecked(True)
        else:
            self.jogPanel.ui.minusButton.setChecked(False)
        if EtcInValue & DOOR_UNLOCK:
            self.jogPanel.ui.doorUnlockButton.setChecked(True)
        else:
            self.jogPanel.ui.doorUnlockButton.setChecked(False)

        #common Buttons
        if EtcInValue & LASER_READY:
            self.autoPanel.ui.laserReadyLed.setChecked(True)
            self.jogPanel.ui.laserReadyLed.setChecked(True)
        else:
            self.autoPanel.ui.laserReadyLed.setChecked(False)
            self.jogPanel.ui.laserReadyLed.setChecked(False)
        if EtcInValue & SERVO:
            self.autoPanel.ui.servoEnableButton.setChecked(True)
            self.jogPanel.ui.servoEnableButton.setChecked(True)
        else:
            self.autoPanel.ui.servoEnableButton.setChecked(False)
            self.jogPanel.ui.servoEnableButton.setChecked(False)
        if EtcInValue & ALM_OVR:
            self.autoPanel.ui.almOvrButton.setChecked(True)
            self.jogPanel.ui.almOvrButton.setChecked(True)
        else:
            self.autoPanel.ui.almOvrButton.setChecked(False)
            self.jogPanel.ui.almOvrButton.setChecked(False)
        if EtcInValue & ALM_RST:
            self.autoPanel.ui.almRstButton.setChecked(True)
            self.jogPanel.ui.almRstButton.setChecked(True)
        else:
            self.autoPanel.ui.almRstButton.setChecked(False)
            self.jogPanel.ui.almRstButton.setChecked(False)
        if EtcInValue & PANEL_DOWN:
            self.autoPanel.ui.panelDownButton.setChecked(True)
            self.jogPanel.ui.panelDownButton.setChecked(True)
        else:
            self.autoPanel.ui.panelDownButton.setChecked(False)
            self.jogPanel.ui.panelDownButton.setChecked(False)
        if EtcInValue & PANEL_UP:
            self.autoPanel.ui.panelUpButton.setChecked(True)
            self.jogPanel.ui.panelUpButton.setChecked(True)
        else:
            self.autoPanel.ui.panelUpButton.setChecked(False)
            self.jogPanel.ui.panelUpButton.setChecked(False)
     


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

    def handle_button_released(self, button_value):
        self.buttonStatus &= ~button_value

    def on_laserOnButton_toggled(self, checked):
        if checked:
            self.autoPanel.ui.laserOnButton.setChecked(True)
            self.jogPanel.ui.laserOnButton.setChecked(True)
            self.buttonStatus |= LASER_ON

        else:
            self.buttonStatus &= ~LASER_ON
            self.autoPanel.ui.laserOnButton.setChecked(False)
            self.jogPanel.ui.laserOnButton.setChecked(False)
    def on_nozzleChangeButton_toggled(self, checked):
        if checked:
            self.jogPanel.ui.nozzleChangeButton.setChecked(True)
            self.buttonStatus |= NOZZLE_CHANGE
        else:
            self.buttonStatus &= ~NOZZLE_CHANGE
            self.jogPanel.ui.nozzleChangeButton.setChecked(False)

    def write_process_data(self, value):
        values = [0, 0]
        values[0] = value & 0xFFFFFFFF
        values[1] = (value >> 32 )& 0xFFFFFFFF
        data = f"0x{values[0]:08X} 0x{values[1]:08X} 0x00000000 0x00000000 0x00000000 0x00000000 0x00000000 0x00000000"
        self.in_file.seek(0)
        self.in_file.write(data)
        self.in_file.flush()  # ensures write is sent immediately

    def read_process_data_first(self):
        self.out_file.seek(0)
        content = self.out_file.read().strip().split()
        first  = int(content[0], 16)
        second = int(content[1], 16)
        return first | (second << 32)


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
