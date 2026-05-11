import os
import sys
import pandas as pd
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, pyqtSignal, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6 import uic

class PatientsFileView(QWidget):
    request_home_page = pyqtSignal()
    action_add_patient = pyqtSignal(str) 
    action_delete_patient = pyqtSignal(str)
    action_undo = pyqtSignal()
    action_redo = pyqtSignal()
    action_search = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'ui/patients_file.ui')
        try:
            uic.loadUi(ui_path, self)
        except FileNotFoundError:
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
        
        self.hide_operation_elements()
        self.close_operation_button.clicked.connect(self.operation_frame.hide)
        
        self.current_operation_mode = None

        self.menu_button.clicked.connect(self.toggle_menu)
        self.menu_patients_file_button.setDisabled(True)

        self.operation_button.clicked.connect(self.route_operation)
        self.add_snp_button.clicked.connect(self.on_open_add_clicked)
        self.remove_snp_button.clicked.connect(self.on_open_delete_clicked)
        self.undo_button.clicked.connect(self.handle_undo)
        self.redo_button.clicked.connect(self.handle_redo)
        self.home_button.clicked.connect(self.open_home)

        self.searchbar_line_edit.returnPressed.connect(self.trigger_search)

    def trigger_search(self):
        search_term = self.searchbar_line_edit.text().strip()
        category = self.search_combobox.currentText()
        self.action_search.emit(category, search_term)

    def populate_table(self, dataframe):
        try:
            if dataframe is None or (isinstance(dataframe, pd.DataFrame) and dataframe.empty):
                self.patients_table_view.setModel(QStandardItemModel(0, 0))
                return

            model = QStandardItemModel(len(dataframe), len(dataframe.columns))
            model.setHorizontalHeaderLabels(dataframe.columns.astype(str).tolist())

            for row_index, row_data in enumerate(dataframe.itertuples(index=False)):
                for col_index, value in enumerate(row_data):
                    item = QStandardItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable) 
                    model.setItem(row_index, col_index, item)

            self.patients_table_view.setModel(model)
        except Exception as e:
            print(f"Table Population Error: {e}")

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

    def hide_operation_elements(self):
        self.operation_frame.hide()

    def on_open_add_clicked(self):
        self.current_operation_mode = "ADD"
        self.operation_button.setText("Add SNP")
        self.operation_title_label.setText("Add SNP to the Patients File")
        self.operation_frame.show()
    
    def on_open_delete_clicked(self):
        self.current_operation_mode = "DELETE"
        self.operation_button.setText("Delete SNP")
        self.operation_title_label.setText("Delete SNP from the Patients File")
        self.operation_frame.show()

    def route_operation(self):
        rsid = self.rsid_input.text()
        Chr = self.chr_input.text()
        Position = self.position_input.text()
        excg46 = self.excg46_input.text()
        if self.current_operation_mode == "ADD":
            self.action_add_patient.emit(f"{rsid}\t{Chr}\t{Position}\t{excg46}")
        elif self.current_operation_mode == "DELETE":
            self.action_delete_patient.emit(f"{rsid}\t{Chr}\t{Position}\t{excg46}")
            
        self.rsid_input.clear()
        self.chr_input.clear()
        self.position_input.clear()
        self.excg46_input.clear()
        self.operation_frame.hide()
        self.current_operation_mode = None

    def handle_undo(self):
        self.action_undo.emit()

    def handle_redo(self):
        self.action_redo.emit()

    def open_home(self):
        self.request_home_page.emit()

    def open_snp_analyser(self):
        pass
    
    def open_patients_statistics(self):
        pass

    def open_grpm_database(self):
        pass

    def open_settings(self):
        pass

    def open_info(self):
        pass