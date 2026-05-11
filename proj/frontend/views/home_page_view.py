import os
import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, pyqtSignal
from PyQt6 import uic

class HomePageView(QWidget):
    request_patients_page = pyqtSignal()
    request_statistics_page = pyqtSignal()

    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'ui/home.ui')
        try:
            uic.loadUi(ui_path, self)
        except FileNotFoundError:
            print(f"Error: Could not find '{ui_path}'")
            sys.exit(1)
            
        self.sidebar_buttons = [
            self.home_button,
            self.menu_snp_analyser_button, 
            self.menu_patients_statistics_button, 
            self.menu_patients_file_button, 
            self.grpm_database_button, 
            self.menu_settings_button, 
            self.menu_info_button
        ]
        self.button_texts = {btn: btn.text() for btn in self.sidebar_buttons}
        
        self.full_sidebar_frame.setMinimumWidth(150)
        self.full_sidebar_frame.setMaximumWidth(150)
        
        self.home_button.setDisabled(True)
        self.menu_button.clicked.connect(self.toggle_menu)
        
        self.menu_patients_file_button.clicked.connect(self.open_patients_file)
        self.menu_patients_statistics_button.clicked.connect(self.open_patients_statistics)

        #date_and_time = QDateTime.currentDateTime().toString("dddd, MMMM d, yyyy - hh:mm AP")
        self.date_and_time_label.setText("DATE AND TIME PLACEHOLDER")    #TO DO

    def toggle_menu(self):
        current_width = self.full_sidebar_frame.width()
        
        if current_width == 150: 
            target_width = 50 
            self.menu_button.setText("≡") 
            for btn in self.sidebar_buttons:
                btn.hide()  
                btn.setEnabled(False)   
        else: 
            target_width = 150
            self.menu_button.setText("Menu")
            for btn in self.sidebar_buttons:
                btn.show()  
                btn.setEnabled(True) 
                
        self.anim_min = QPropertyAnimation(self.full_sidebar_frame, b"minimumWidth")
        self.anim_min.setDuration(300)
        self.anim_min.setStartValue(current_width)
        self.anim_min.setEndValue(target_width)
        self.anim_min.setEasingCurve(QEasingCurve.Type.InOutQuart) 
        
        self.anim_max = QPropertyAnimation(self.full_sidebar_frame, b"maximumWidth")
        self.anim_max.setDuration(300)
        self.anim_max.setStartValue(current_width)
        self.anim_max.setEndValue(target_width)
        self.anim_max.setEasingCurve(QEasingCurve.Type.InOutQuart)
        
        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim_min)
        self.anim_group.addAnimation(self.anim_max)
        
        self.anim_group.start()

    def open_patients_file(self):
        self.request_patients_page.emit()

    def open_snp_analyser(self):
        pass

    def open_patients_statistics(self):
        self.request_statistics_page.emit()

    def open_grpm_database(self):
        pass

    def open_settings(self):
        pass

    def open_info(self):
        pass