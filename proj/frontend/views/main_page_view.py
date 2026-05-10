import os
import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6 import uic

class MainPageView(QWidget):
    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'ui/main_page.ui')
        try:
            uic.loadUi(ui_path, self)
        except FileNotFoundError:
            print(f"Error: Could not find '{ui_path}'")
            sys.exit(1)

        self.start_app_button.clicked.connect(self.on_start_clicked)

    def on_start_clicked(self):
        self.start_app_button.setText("Loading...")

    def resizeEvent(self, event):
            super().resizeEvent(event)
            raw_ratio = self.width() / 678.0
            scale_ratio = 1.0 + ((raw_ratio - 1.0) * 0.5)
            scale_ratio = max(1.0, min(scale_ratio, 1.4))

            new_title_size = int(28 * scale_ratio)
            title_font = self.title_label.font()
            title_font.setPointSize(new_title_size)
            self.title_label.setFont(title_font)

            new_btn_font_size = int(20 * scale_ratio)
            btn_font = self.start_app_button.font()
            btn_font.setPointSize(new_btn_font_size)
            self.start_app_button.setFont(btn_font)

            new_btn_width = int(250 * scale_ratio)
            new_btn_height = int(70 * scale_ratio)
            self.start_app_button.setFixedSize(new_btn_width, new_btn_height)