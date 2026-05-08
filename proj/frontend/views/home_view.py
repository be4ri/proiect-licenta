from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal

class HomeView(QWidget):
    # Create a custom signal that shouts "Change the page!" when triggered
    go_to_settings_signal = pyqtSignal()
    go_to_patients_statistics_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # The button that will take us to the next page
        self.nav_button = QPushButton("Go to Settings Page ➡️")
        layout.addWidget(self.nav_button)

        label = QLabel("🏠 Welcome to the Home Page!")
        label.setObjectName("header") # <--- Add this!
        layout.addWidget(label)

        self.patients_statistics_button = QPushButton("Go to Patients Statistics Page ➡️")
        layout.addWidget(self.patients_statistics_button)



        # When clicked, emit our custom signal
        self.nav_button.clicked.connect(self.go_to_settings_signal.emit)
        self.patients_statistics_button.clicked.connect(self.go_to_patients_statistics_signal.emit)