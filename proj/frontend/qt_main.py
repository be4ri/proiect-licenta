import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

# 1. Path Setup
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from views.patients_statistics_view import PatientsStatisticsView
from views.home_view import HomeView
from views.settings_view import SettingsView

class ThesisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thesis AI Dashboard")
        
        # Create the Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize the pages
        self.home_page = HomeView()
        self.settings_page = SettingsView()
        self.patients_statistics_page = PatientsStatisticsView()

        # Add pages to the stack
        self.stacked_widget.addWidget(self.home_page)              # Index 0
        self.stacked_widget.addWidget(self.settings_page)          # Index 1
        self.stacked_widget.addWidget(self.patients_statistics_page) # Index 2

        # Connections
        self.home_page.go_to_settings_signal.connect(self.show_settings_page)
        self.home_page.go_to_patients_statistics_signal.connect(self.show_patients_statistics_page)
        self.settings_page.go_to_home_signal.connect(self.show_home_page)
        self.patients_statistics_page.go_to_home_signal.connect(self.show_home_page)
        self.patients_statistics_page.go_to_settings_signal.connect(self.show_settings_page)

    def show_settings_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_home_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_patients_statistics_page(self):
        self.stacked_widget.setCurrentIndex(2)

# --- Improved Style Loader ---
def load_stylesheets(app):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files = [
        os.path.join(current_dir, "styles", "darktheme.qss"),
        os.path.join(current_dir, "styles", "top_bar.qss")
    ]
    
    combined_qss = ""
    for path in files:
        if os.path.exists(path):
            with open(path, "r") as f:
                combined_qss += f.read() + "\n"
        else:
            print(f"Warning: Style file not found at {path}")
    
    app.setStyleSheet(combined_qss)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load all styles at once to avoid overwriting
    load_stylesheets(app)
    
    window = ThesisApp()
    window.showFullScreen()
    sys.exit(app.exec())