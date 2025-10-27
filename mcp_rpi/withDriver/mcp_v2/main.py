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

PANEL_UP = 1 << 33
PANEL_DOWN = 1 << 34
NOZZLE_CHANGE = 1 << 35

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

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Password")
        self.setFixedSize(400, 600)
        self.layout = QVBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setMinimumSize(350, 60)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter numeric password")
        self.password_input.setAlignment(Qt.AlignCenter)
        self.warning_label = QLabel("")
        self.warning_label.setAlignment(Qt.AlignCenter)
        self.warning_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #d9534f;
                border-radius: 8px;
                padding: 6px;
                font-size: 18px;
            }
        """)
        self.warning_label.hide()
        keypad_layout = QGridLayout()
        buttons = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '0', 'Clear', 'Enter']
        positions = [(i // 3, i % 3) for i in range(9)] + [(3, 0), (3, 1), (3, 2)]
        for i, btn_text in enumerate(buttons):
            button = QPushButton(btn_text)
            button.setMinimumSize(80, 60)
            button.setStyleSheet("font-size: 18px;")
            button.clicked.connect(self.button_clicked)
            keypad_layout.addWidget(button, *positions[i])
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.warning_label)
        self.layout.addLayout(keypad_layout)
        self.setLayout(self.layout)

    def show_warning(self, text):
        self.warning_label.setText(text)
        self.warning_label.show()
        QTimer.singleShot(1000, self.warning_label.hide)

    def button_clicked(self):
        button = self.sender()
        if not button:
            return
        text = button.text()
        if text == "Enter":
            if self.password_input.text() == "1234":
                self.accept()
            else:
                self.show_warning("Incorrect password")
                self.password_input.clear()
        elif text == "Clear":
            self.password_input.clear()
        else:
            self.password_input.setText(self.password_input.text() + text)

class SettingsDialog(QDialog):
    settings_saved = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setModal(True)
        self.layout = QVBoxLayout()

        # Store previous and current settings
        self.previous_settings = {}
        self.current_x = -60
        self.current_y = 10
        self.current_width = 650
        self.current_height = 450

        # Timer for throttling updates
        self.update_timer = QTimer(self)
        self.update_timer.setSingleShot(True)
        self.update_timer.setInterval(200)  # 200ms delay
        self.update_timer.timeout.connect(self.apply_temp_settings)

        # Repeat timers for long press
        self.repeat_timer_horizontal = QTimer(self)
        self.repeat_timer_horizontal.timeout.connect(self.repeat_action)  # Fixed to connect to repeat_action
        self.repeat_timer_vertical = QTimer(self)
        self.repeat_timer_vertical.timeout.connect(self.repeat_action)  # Fixed to connect to repeat_action
        self.repeat_direction = 0  # 1 for plus, -1 for minus
        self.repeat_step = 10  # Initial step
        self.repeat_fast_step = 50  # Faster step for long press
        self.repeat_initial_delay = 500  # ms before first repeat
        self.repeat_interval = 100  # ms between repeats
        self.repeat_count = 0  # To detect long press

        # Language selection
        self.language_label = QLabel("Select Language:")
        self.language_label.setStyleSheet("font-size: 18px;")
        self.language_combo = QComboBox()
        self.language_combo.setMinimumSize(450, 60)
        self.language_combo.setStyleSheet("font-size: 18px;")
        self.language_combo.addItems(["English", "Japanese"])

        # Logo selection
        self.logo_label = QLabel("Company Logo:")
        self.logo_label.setStyleSheet("font-size: 18px;")
        self.logo_path_edit = QLineEdit()
        self.logo_path_edit.setMinimumSize(350, 60)
        self.logo_path_edit.setReadOnly(True)
        self.browse_button = QPushButton("Browse")
        self.browse_button.setMinimumSize(80, 60)
        self.browse_button.setStyleSheet("font-size: 18px;")
        self.browse_button.clicked.connect(self.browse_logo)
        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.logo_path_edit)
        logo_layout.addWidget(self.browse_button)

        # Logo adjustment selection
        self.adjust_label = QLabel("Adjust:")
        self.adjust_label.setStyleSheet("font-size: 18px;")
        self.adjust_combo = QComboBox()
        self.adjust_combo.setMinimumSize(450, 60)
        self.adjust_combo.setStyleSheet("font-size: 18px;")
        self.adjust_combo.addItems(["Position", "Size"])
        self.adjust_combo.currentTextChanged.connect(self.update_controls)

        # Horizontal controls (x or width)
        self.horizontal_label = QLabel("X: -60")
        self.horizontal_label.setStyleSheet("font-size: 18px;")
        self.horizontal_minus_button = QPushButton("-")
        self.horizontal_minus_button.setFixedSize(60, 60)
        self.horizontal_minus_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: 2px solid #388E3C;
                border-radius: 10px;
                font-size: 24px;
                color: white;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        self.horizontal_minus_button.pressed.connect(lambda: self.start_repeat(-1, 'horizontal'))
        self.horizontal_minus_button.released.connect(self.stop_repeat)
        self.horizontal_plus_button = QPushButton("+")
        self.horizontal_plus_button.setFixedSize(60, 60)
        self.horizontal_plus_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: 2px solid #388E3C;
                border-radius: 10px;
                font-size: 24px;
                color: white;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        self.horizontal_plus_button.pressed.connect(lambda: self.start_repeat(1, 'horizontal'))
        self.horizontal_plus_button.released.connect(self.stop_repeat)

        # Vertical controls (y or height)
        self.vertical_label = QLabel("Y: 10")
        self.vertical_label.setStyleSheet("font-size: 18px;")
        self.vertical_minus_button = QPushButton("-")
        self.vertical_minus_button.setFixedSize(60, 60)
        self.vertical_minus_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: 2px solid #388E3C;
                border-radius: 10px;
                font-size: 24px;
                color: white;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        self.vertical_minus_button.pressed.connect(lambda: self.start_repeat(-1, 'vertical'))
        self.vertical_minus_button.released.connect(self.stop_repeat)
        self.vertical_plus_button = QPushButton("+")
        self.vertical_plus_button.setFixedSize(60, 60)
        self.vertical_plus_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: 2px solid #388E3C;
                border-radius: 10px;
                font-size: 24px;
                color: white;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        self.vertical_plus_button.pressed.connect(lambda: self.start_repeat(1, 'vertical'))
        self.vertical_plus_button.released.connect(self.stop_repeat)

        # Controls layout
        controls_layout = QHBoxLayout()
        horizontal_controls = QHBoxLayout()
        horizontal_controls.addWidget(self.horizontal_label)
        horizontal_controls.addWidget(self.horizontal_minus_button)
        horizontal_controls.addWidget(self.horizontal_plus_button)
        horizontal_controls.addStretch()
        vertical_controls = QHBoxLayout()
        vertical_controls.addWidget(self.vertical_label)
        vertical_controls.addWidget(self.vertical_minus_button)
        vertical_controls.addWidget(self.vertical_plus_button)
        controls_layout.addLayout(horizontal_controls)
        controls_layout.addStretch()
        controls_layout.addLayout(vertical_controls)

        # Buttons
        button_layout = QHBoxLayout()
        applyButton = QPushButton("Apply")
        closeButton = QPushButton("Close")
        applyButton.setMinimumSize(100, 60)
        applyButton.setStyleSheet("font-size: 18px;")
        closeButton.setMinimumSize(100, 60)
        closeButton.setStyleSheet("font-size: 18px;")
        button_layout.addStretch()
        button_layout.addWidget(applyButton)
        button_layout.addWidget(closeButton)
        applyButton.clicked.connect(self.save_settings)
        closeButton.clicked.connect(self.restore_previous_settings)

        self.load_settings()
        self.layout.addWidget(self.language_label)
        self.layout.addWidget(self.language_combo)
        self.layout.addWidget(self.logo_label)
        self.layout.addLayout(logo_layout)
        self.layout.addWidget(self.adjust_label)
        self.layout.addWidget(self.adjust_combo)
        self.layout.addLayout(controls_layout)
        self.layout.addStretch()
        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def load_settings(self):
        config_file = "settings.json"
        default_language = "English"
        default_logo_path = ""
        default_x = -60
        default_y = 10
        default_width = 650
        default_height = 450
        self.previous_settings = {
            "language": default_language,
            "logo_path": default_logo_path,
            "logo_x": default_x,
            "logo_y": default_y,
            "logo_width": default_width,
            "logo_height": default_height
        }
        self.current_x = default_x
        self.current_y = default_y
        self.current_width = default_width
        self.current_height = default_height
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    self.previous_settings.update({
                        "language": config.get("language", default_language),
                        "logo_path": config.get("logo_path", default_logo_path),
                        "logo_x": config.get("logo_x", default_x),
                        "logo_y": config.get("logo_y", default_y),
                        "logo_width": config.get("logo_width", default_width),
                        "logo_height": config.get("logo_height", default_height)
                    })
                    self.current_x = self.previous_settings["logo_x"]
                    self.current_y = self.previous_settings["logo_y"]
                    self.current_width = self.previous_settings["logo_width"]
                    self.current_height = self.previous_settings["logo_height"]
                    if self.previous_settings["language"] in ["English", "Japanese"]:
                        self.language_combo.setCurrentText(self.previous_settings["language"])
                    self.logo_path_edit.setText(self.previous_settings["logo_path"])
                    self.adjust_combo.setCurrentText("Position")  # Default to Position
                    self.update_controls("Position")
            except (json.JSONDecodeError, KeyError):
                self.language_combo.setCurrentText(default_language)
                self.logo_path_edit.setText(default_logo_path)
                self.adjust_combo.setCurrentText("Position")
                self.update_controls("Position")

    def update_controls(self, selection):
        if selection == "Position":
            self.horizontal_label.setText(f"X: {self.current_x}")
            self.vertical_label.setText(f"Y: {self.current_y}")
        else:  # Size
            self.horizontal_label.setText(f"Width: {self.current_width}")
            self.vertical_label.setText(f"Height: {self.current_height}")

    def start_repeat(self, direction, orientation):
        self.repeat_direction = direction
        self.repeat_orientation = orientation
        self.repeat_count = 0
        self.repeat_step = 10
        self.repeat_action()
        if orientation == 'horizontal':
            self.repeat_timer_horizontal.start(self.repeat_initial_delay)
        else:
            self.repeat_timer_vertical.start(self.repeat_initial_delay)

    def stop_repeat(self):
        self.repeat_timer_horizontal.stop()
        self.repeat_timer_vertical.stop()
        self.repeat_direction = 0

    def repeat_action(self):
        if self.repeat_direction == 0:
            return
        if self.repeat_orientation == 'horizontal':
            if self.adjust_combo.currentText() == "Position":
                self.current_x = max(-1920, min(1920, self.current_x + self.repeat_direction * self.repeat_step))
                self.horizontal_label.setText(f"X: {self.current_x}")
            else:
                self.current_width = max(50, min(1920, self.current_width + self.repeat_direction * self.repeat_step))
                self.horizontal_label.setText(f"Width: {self.current_width}")
        else:  # vertical
            if self.adjust_combo.currentText() == "Position":
                self.current_y = max(-720, min(720, self.current_y + self.repeat_direction * self.repeat_step))
                self.vertical_label.setText(f"Y: {self.current_y}")
            else:
                self.current_height = max(50, min(720, self.current_height + self.repeat_direction * self.repeat_step))
                self.vertical_label.setText(f"Height: {self.current_height}")
        self.schedule_update()
        self.repeat_count += 1
        if self.repeat_count > 5:
            self.repeat_step = 50  # Faster step after initial presses

    def schedule_update(self):
        self.update_timer.start()  # Restart timer on action

    def apply_temp_settings(self):
        if self.current_width < 50 or self.current_height < 50:
            return  # Prevent invalid sizes
        self.parent().set_logo(self.logo_path_edit.text(), self.current_x, self.current_y, self.current_width, self.current_height)

    def save_settings(self):
        language = self.language_combo.currentText()
        logo_path = self.logo_path_edit.text()
        if self.current_width < 50 or self.current_height < 50:
            QMessageBox.warning(self, "Invalid Size", "Width and height must be at least 50 pixels.")
            return
        config_file = "settings.json"
        self.previous_settings.update({
            "language": language,
            "logo_path": logo_path,
            "logo_x": self.current_x,
            "logo_y": self.current_y,
            "logo_width": self.current_width,
            "logo_height": self.current_height
        })
        with open(config_file, "w") as f:
            json.dump(self.previous_settings, f, indent=2)
        self.settings_saved.emit()

    def restore_previous_settings(self):
        self.parent().set_logo(
            self.previous_settings["logo_path"],
            self.previous_settings["logo_x"],
            self.previous_settings["logo_y"],
            self.previous_settings["logo_width"],
            self.previous_settings["logo_height"]
        )
        self.reject()

    def browse_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Logo Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.svg)")
        if file_path:
            self.logo_path_edit.setText(file_path)
            self.apply_temp_settings()

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
        for page in (self.home1, self.home2):
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
            if hasattr(self.home1.ui, 'logoLable') and isinstance(self.home1.ui.logoLable, QLabel):
                self.home1.ui.logoLable.setPixmap(pixmap)
                self.home1.ui.logoLable.setGeometry(x, y, width, height)
            # Update logoLable for Home2Widget if it exists
            if hasattr(self.home2.ui, 'logoLable') and isinstance(self.home2.ui.logoLable, QLabel):
                self.home2.ui.logoLable.setPixmap(pixmap)
                self.home2.ui.logoLable.setGeometry(x, y, width, height)
        else:
            # Apply geometry even if no logo is set
            if hasattr(self.home1.ui, 'logoLable') and isinstance(self.home1.ui.logoLable, QLabel):
                self.home1.ui.logoLable.setGeometry(x, y, width, height)
            if hasattr(self.home2.ui, 'logoLable') and isinstance(self.home2.ui.logoLable, QLabel):
                self.home2.ui.logoLable.setGeometry(x, y, width, height)

    def open_password_dialog(self):
        password_dialog = PasswordDialog(self)
        if password_dialog.exec() == QDialog.Accepted:
            self.open_settings()

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.settings_saved.connect(self.apply_settings)
        dialog.exec()

    def init_buttons(self):
        self.home1.ui.laserReadyLed.setEnabled(False)
        self.home2.ui.laserReadyLed.setEnabled(False)
        # self.set_autoMode_buttons(False)
        # Navigation
        self.home1.ui.jogButton.pressed.connect(
            lambda: (self.stacked_central.setCurrentWidget(self.home2),
                    self.handle_button_pressed(JOG),
                    )
        )
        # self.set_jogMode_buttons(False)
        self.home1.ui.autoButton.pressed.connect(
            lambda: (self.stacked_central.setCurrentWidget(self.home1),
                    self.handle_button_pressed(AUTO)
                    )
                    # self.set_autoMode_buttons(False)
        )
        self.home2.ui.jogButton.pressed.connect(
            lambda: (self.stacked_central.setCurrentWidget(self.home2),
                    self.handle_button_pressed(JOG)
                    # self.set_jogMode_buttons(False)
                   )
        )
        self.home2.ui.autoButton.pressed.connect(
            lambda: (self.stacked_central.setCurrentWidget(self.home1),
                    self.handle_button_pressed(AUTO)
                    # self.set_autoMode_buttons(False)
                    )
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
        self.home2.ui.nozzleBoxButton.pressed.connect(
            lambda: self.handle_button_pressed(NOZZLE_CHANGE)
        )

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
        self.home1.ui.settingButton.clicked.connect(self.open_password_dialog)
        self.home1.ui.panelDownButton.pressed.connect(
            lambda: self.handle_button_pressed(PANEL_DOWN)
        )
        self.home1.ui.panelUpButton.pressed.connect(
            lambda: self.handle_button_pressed(PANEL_UP)
        )
        

        self.home2.ui.settingButton.clicked.connect(self.open_password_dialog)
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
        self.home2.ui.panelDownButton.pressed.connect(
            lambda: self.handle_button_pressed(PANEL_DOWN)
        )
        self.home2.ui.panelUpButton.pressed.connect(
            lambda: self.handle_button_pressed(PANEL_UP)
        )
       
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
        self.home2.ui.nozzleBoxButton.released.connect(
            lambda: self.handle_button_released(NOZZLE_CHANGE)
        )

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
        self.home1.ui.panelDownButton.released.connect(
            lambda: self.handle_button_released(PANEL_DOWN)
        )
        self.home1.ui.panelUpButton.released.connect(
            lambda: self.handle_button_released(PANEL_UP)
        )
        self.home2.ui.panelDownButton.released.connect(
            lambda: self.handle_button_released(PANEL_DOWN)
        )
        self.home2.ui.panelUpButton.released.connect(
            lambda: self.handle_button_released(PANEL_UP)
        )



        self.home1.ui.autoButton.released.connect(lambda: self.handle_button_released(AUTO))
        self.home1.ui.jogButton.released.connect(lambda: self.handle_button_released(JOG))
        self.home2.ui.autoButton.released.connect(lambda: self.handle_button_released(AUTO))
        self.home2.ui.jogButton.released.connect(lambda: self.handle_button_released(JOG))

    def update_button_states(self, EtcInValue):
        if EtcInValue & AUTO:
            # self.set_autoMode_buttons(True)
            # self.set_jogMode_buttons(True)
            self.stacked_central.setCurrentWidget(self.home1)
        elif EtcInValue & JOG:
            # self.set_jogMode_buttons(True)
            # self.set_autoMode_buttons(True)
            self.stacked_central.setCurrentWidget(self.home2)
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
        if EtcInValue & PANEL_DOWN:
            self.home1.ui.panelDownButton.setChecked(True)
            self.home2.ui.panelDownButton.setChecked(True)
        else:
            self.home1.ui.panelDownButton.setChecked(False)
            self.home2.ui.panelDownButton.setChecked(False)
        if EtcInValue & PANEL_UP:
            self.home1.ui.panelUpButton.setChecked(True)
            self.home2.ui.panelUpButton.setChecked(True)
        else:
            self.home1.ui.panelUpButton.setChecked(False)
            self.home2.ui.panelUpButton.setChecked(False)
        if EtcInValue & NOZZLE_CHANGE:
            self.home2.ui.nozzleBoxButton.setChecked(True)
        else:
            self.home2.ui.nozzleBoxButton.setChecked(False)


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
        # self.write_process_data(self.buttonStatus)

    def handle_button_released(self, button_value):
        self.buttonStatus &= ~button_value
        # self.write_process_data(self.buttonStatus)

    def on_laserOnButton_toggled(self, checked):
        if checked:
            self.home1.ui.laserOnButton.setChecked(True)
            self.home2.ui.laserOnButton.setChecked(True)
            self.buttonStatus |= LASER_ON

        else:
            self.buttonStatus &= ~LASER_ON
            self.home1.ui.laserOnButton.setChecked(False)
            self.home2.ui.laserOnButton.setChecked(False)
        # self.write_process_data(self.buttonStatus)
    

    def write_process_data(self, value, path="/sys/bus/spi/devices/spi0.0/process_data_in"):
        values = [0, 0]
        values[0] = value & 0xFFFFFFFF
        values[1] = (value >> 32 )& 0xFFFFFFFF
        # Create a string with the first value as the input, others as 0x00000000
        data = f"0x{values[0]:08X} 0x{values[1]:08X} 0x00000000 0x00000000 0x00000000 0x00000000 0x00000000 0x00000000"
        print(f"Writing process data: {data}")
        with open(path, "w") as f:
            f.write(data)  # Add newline to ensure proper write

    def read_process_data_first(self, path="/sys/bus/spi/devices/spi0.0/process_data_out"):
        with open(path, "r") as f:
            content = f.read().strip()
        first_hex = content.split()[0]
        second_hex = content.split()[1]
        print(f"Read process data: {content}")
        print(f"First hex: {first_hex}, Second hex: {second_hex}")
        value = int(first_hex, 16) | (int(second_hex, 16) << 32)
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