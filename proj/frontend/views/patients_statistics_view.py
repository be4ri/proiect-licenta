from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import pyqtSignal, Qt

class PatientsStatisticsView(QWidget):
    go_to_home_signal = pyqtSignal()
    go_to_settings_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Main vertical layout for the whole page
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) 
        main_layout.setSpacing(0)

        # --- TOP BAR SETUP ---
        self.top_bar = QFrame()
        self.top_bar.setObjectName("topBar") # Matches #topBar in QSS
        
        top_bar_layout = QHBoxLayout(self.top_bar)
        top_bar_layout.setContentsMargins(15, 0, 15, 0)
        top_bar_layout.setSpacing(10)

        # Buttons
        self.back_button = QPushButton("⬅️ Back to Home")
        self.back_button.setObjectName("topbarbutton") # Matches #topbarbutton in QSS
        
        self.settings_button = QPushButton("⚙️ Go to Settings")
        self.settings_button.setObjectName("topbarbutton")

        # Add buttons to bar and push them to the left with a stretch
        top_bar_layout.addWidget(self.back_button)
        top_bar_layout.addWidget(self.settings_button)
        top_bar_layout.addStretch()

        # --- BODY CONTENT ---
        # Container for the rest of the page to add padding
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        
        self.header_label = QLabel("📊 Patients Statistics Page")
        self.header_label.setObjectName("header")
        
        content_layout.addWidget(self.header_label, 0, Qt.AlignmentFlag.AlignHCenter)
        content_layout.addStretch() # Pushes label to the top of the content area

        # --- ASSEMBLY ---
        main_layout.addWidget(self.top_bar)      # Top Bar stays at the top
        main_layout.addWidget(content_container) # Rest of the content below

        # Connections
        self.back_button.clicked.connect(self.go_to_home_signal.emit)
        self.settings_button.clicked.connect(self.go_to_settings_signal.emit)