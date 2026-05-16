import os
import sys
import pandas as pd
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, pyqtSignal, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6 import uic

class StatisticsView(QWidget):
    request_home_page = pyqtSignal()
    request_patients_page = pyqtSignal()
    action_request_table = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'ui/statistics.ui')
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

        self.menu_button.clicked.connect(self.toggle_menu)
        self.menu_patients_statistics_button.setDisabled(True)

        self.home_button.clicked.connect(self.open_home)
        self.menu_patients_file_button.clicked.connect(self.open_patients_file)

        self.view_matching_snps_button.clicked.connect(lambda: self.action_request_table.emit("Matching SNPs"))
        self.pushButton.clicked.connect(lambda: self.action_request_table.emit("MeSH Statistics"))
        self.shannon_mesh_per_snp_button.clicked.connect(lambda: self.action_request_table.emit("Shannon Index per SNP"))
        self.shannon_snp_per_Mesh.clicked.connect(lambda: self.action_request_table.emit("Shannon Index per MeSH Term"))

    def update_matching_count_label(self, count):
        base_text = "The number of SNPs from the patients' file that are found in the GRPM Nutrigen dataset: "
        self.nr_of_snps_label.setText(f"{base_text} {count}")

    def populate_table(self, dataframe):
        try:
            if dataframe is None or (isinstance(dataframe, pd.DataFrame) and dataframe.empty) or (isinstance(dataframe, pd.Series) and dataframe.empty):
                self.statistics_table.setModel(QStandardItemModel(0, 0))
                return

            if isinstance(dataframe, pd.Series):
                dataframe = dataframe.to_frame(name="GRPM_RSID")

            model = QStandardItemModel(len(dataframe), len(dataframe.columns))
            model.setHorizontalHeaderLabels(dataframe.columns.astype(str).tolist())

            for row_index, row_data in enumerate(dataframe.itertuples(index=False)):
                for col_index, value in enumerate(row_data):
                    item = QStandardItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable) 
                    model.setItem(row_index, col_index, item)

            self.statistics_table.setModel(model)
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

    def open_home(self):
        self.request_home_page.emit()

    def open_patients_file(self):
        self.request_patients_page.emit()