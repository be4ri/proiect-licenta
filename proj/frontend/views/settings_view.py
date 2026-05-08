from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import pyqtSignal

class SettingsView(QWidget):
    go_to_home_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # The button to go back
        self.back_button = QPushButton("⬅️ Back to Home")
        layout.addWidget(self.back_button)

        label = QLabel("⚙️ SETTINGS")
        label.setObjectName("header")
        layout.addWidget(label)



        # When clicked, emit the signal to go back
        self.back_button.clicked.connect(self.go_to_home_signal.emit)