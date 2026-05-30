import os
import sys
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, pyqtSignal
from PyQt6 import uic

class PatientsAIAnalyserView(QWidget):
    request_home_page = pyqtSignal()
    request_patients_page = pyqtSignal()
    request_statistics_page = pyqtSignal()
    action_analyse = pyqtSignal()

    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'ui/patient_ai_analyser.ui')
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
        
        self.full_sidebar_frame.setMinimumWidth(150)
        self.full_sidebar_frame.setMaximumWidth(150)
        
        self.menu_snp_analyser_button.setDisabled(True)
        
        self.menu_button.clicked.connect(self.toggle_menu)
        
        self.home_button.clicked.connect(self.open_home_page)
        self.menu_patients_file_button.clicked.connect(self.open_patients_file)
        self.menu_patients_statistics_button.clicked.connect(self.open_patients_statistics)

        self.operation_frame.hide()
        self.close_operation_button.clicked.connect(self.hide_operation_panel)
        self.change_model_button.clicked.connect(self.show_operation_panel)
        
        self.analyse_button.clicked.connect(self.trigger_analysis)

    def toggle_menu(self):
        current_width = self.full_sidebar_frame.width()
        
        if current_width == 150: 
            target_width = 50 
            self.menu_button.setText("\u2261") 
            for btn in self.sidebar_buttons:
                btn.hide()  
                btn.setEnabled(False)   
        else: 
            target_width = 150
            self.menu_button.setText("Menu")
            for btn in self.sidebar_buttons:
                btn.show()  
                btn.setEnabled(True) 
            
            self.menu_snp_analyser_button.setDisabled(True)
                
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

    def hide_operation_panel(self):
        self.operation_frame.hide()

    def show_operation_panel(self):
        self.operation_frame.show()

    def trigger_analysis(self):
        self.action_analyse.emit()

    def open_home_page(self):
        self.request_home_page.emit()

    def open_patients_file(self):
        self.request_patients_page.emit()

    def open_patients_statistics(self):
        self.request_statistics_page.emit()