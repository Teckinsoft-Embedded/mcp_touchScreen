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
