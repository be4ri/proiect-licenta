import os
import sys

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt6 import uic

class HomePageView(QWidget):
    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'ui/home.ui')
        try:
            uic.loadUi(ui_path, self)
        except FileNotFoundError:
            print(f"Error: Could not find '{ui_path}'")
            sys.exit(1)
            
        # 1. Group all the target buttons (updated to match your new UI names)
        # Store their original text so we can restore them when the menu re-opens.
        self.sidebar_buttons = [
            self.menu_snp_analyser_button, 
            self.menu_patients_statistics_button, 
            self.menu_patients_file_button, 
            self.grpm_database_button, 
            self.menu_settings_button, 
            self.menu_info_button
        ]
        self.button_texts = {btn: btn.text() for btn in self.sidebar_buttons}
        
        # 2. Set the initial "Open" width of the sidebar (e.g., 150 pixels)
        self.full_sidebar_frame.setMinimumWidth(150)
        self.full_sidebar_frame.setMaximumWidth(150)
        
        # 3. Connect the menu button to our toggle function
        self.menu_button.clicked.connect(self.toggle_menu)

    def toggle_menu(self):
        # Get the current width to determine our starting point
        current_width = self.full_sidebar_frame.width()
        
        if current_width == 150: 
            # THE MENU IS OPEN -> WE MUST CLOSE IT
            target_width = 50 # Shrink to 50 pixels
            self.menu_button.setText("≡") # Change to a small hamburger icon
            
            # Remove text and disable the buttons so they can't be clicked
            for btn in self.sidebar_buttons:
                btn.setText("") 
                btn.setEnabled(False) 
                
        else: 
            # THE MENU IS CLOSED -> WE MUST OPEN IT
            target_width = 150
            self.menu_button.setText("Menu") # Restore menu button text
            
            # Restore original text and enable the buttons
            for btn in self.sidebar_buttons:
                btn.setText(self.button_texts[btn]) 
                btn.setEnabled(True) 
                
        # 4. Create animations for both minimum and maximum width to push the layout
        self.anim_min = QPropertyAnimation(self.full_sidebar_frame, b"minimumWidth")
        self.anim_min.setDuration(300) # Speed in milliseconds
        self.anim_min.setStartValue(current_width)
        self.anim_min.setEndValue(target_width)
        self.anim_min.setEasingCurve(QEasingCurve.Type.InOutQuart) 
        
        self.anim_max = QPropertyAnimation(self.full_sidebar_frame, b"maximumWidth")
        self.anim_max.setDuration(300)
        self.anim_max.setStartValue(current_width)
        self.anim_max.setEndValue(target_width)
        self.anim_max.setEasingCurve(QEasingCurve.Type.InOutQuart)
        
        # 5. Group the animations together so they run simultaneously
        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim_min)
        self.anim_group.addAnimation(self.anim_max)
        
        # Start the sliding animation
        self.anim_group.start()