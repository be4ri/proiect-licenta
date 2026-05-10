import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
import qdarkstyle

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from views.home_page_view import HomePageView
from views.patients_file_view import PatientsFileView
import logic.analyzer as analyzer
import logic.add_snp_command as add_snp_command
import logic.remove_snp_command as remove_snp_command
import logic.snp_command_invoker as snp_command_invoker
import logic.filtering_patient_snp as filtering_patient_snp

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.analyzer_instance = analyzer.Analyzer()
        self.editor = snp_command_invoker.SNPCommandInvoker(self.analyzer_instance.patients_panel)
        self.filtering_patients_instance = filtering_patient_snp.FilteringPatientSNP()

        self.setWindowTitle("--")
        self.resize(800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_page = HomePageView()
        self.patients_page = PatientsFileView()

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.patients_page)

        self.home_page.request_patients_page.connect(self.go_to_patients)
        self.patients_page.request_home_page.connect(self.go_to_home)
        self.patients_page.action_add_patient.connect(self.handle_add_snp)
        self.patients_page.action_delete_patient.connect(self.handle_remove_snp)
        self.patients_page.action_undo.connect(self.handle_undo)
        self.patients_page.action_redo.connect(self.handle_redo)
        
        self.stacked_widget.setCurrentWidget(self.home_page)

    def go_to_patients(self):
        self.stacked_widget.setCurrentWidget(self.patients_page)

    def go_to_home(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def handle_add_snp(self, data_string):
        try:
            GRPM_RSID, Chr, Position, EXCG46 = data_string.split('\t')
        except ValueError:
            return
        
        add_command = add_snp_command.AddSNPCommand(self.analyzer_instance.patients_panel, GRPM_RSID, Chr, Position, EXCG46)
        self.editor.execute_add(GRPM_RSID, Chr, Position, EXCG46)

    def handle_remove_snp(self, data_string):
        try:
            GRPM_RSID, Chr, Position, EXCG46 = data_string.split('\t')
        except ValueError:
            return
            
        remove_command = remove_snp_command.RemoveSNPCommand(self.analyzer_instance.patients_panel, GRPM_RSID, Chr, Position, EXCG46)
        self.editor.execute_remove(GRPM_RSID, Chr, Position, EXCG46)
    
    def handle_undo(self):
        self.editor.undo()
    
    def handle_redo(self):
        self.editor.redo()

    def handle_filter_patients_by_rsid(self, rsid):
        return self.filtering_patients_instance.filter_by_rsid(rsid)
    
    def handle_filter_patients_by_chr(self, chr_val):
        return self.filtering_patients_instance.filter_by_chr(chr_val)
    
    def handle_filter_patients_by_position(self, position):
        return self.filtering_patients_instance.filter_by_position(position)
    
    def handle_filter_patients_by_excg46(self, excg46):
        return self.filtering_patients_instance.filter_by_excg46(excg46)

def main():
    app = QApplication(sys.argv)
    dark_stylesheet = qdarkstyle.load_stylesheet_pyside6()
    app.setStyleSheet(dark_stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()