import sys
import os
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor, QBrush
from PyQt6.QtCore import Qt
import qdarkstyle

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from views.home_page_view import HomePageView
from views.patients_file_view import PatientsFileView
from views.statistics_view import StatisticsView
from views.patients_ai_analyser_view import PatientsAIAnalyserView

import logic.analyzer as analyzer
import logic.add_snp_command as add_snp_command
import logic.remove_snp_command as remove_snp_command
import logic.snp_command_invoker as snp_command_invoker
import logic.filtering_patient_snp as filtering_patient_snp
from logic.engine import GenomicEngine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.analyzer_instance = analyzer.Analyzer()
        self.editor = snp_command_invoker.SNPCommandInvoker(self.analyzer_instance.patients_panel)
        self.filtering_patients_instance = filtering_patient_snp.FilteringPatientSNP()

        try:
            self.ai_engine = GenomicEngine()
        except Exception as e:
            print(f"Failed to load AI Engine: {e}")
            self.ai_engine = None

        self.setWindowTitle("Genomic AI Dashboard")
        self.resize(800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_page = HomePageView()
        self.patients_page = PatientsFileView()
        self.statistics_page = StatisticsView()
        self.ai_analyser_page = PatientsAIAnalyserView()

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.patients_page)
        self.stacked_widget.addWidget(self.statistics_page)
        self.stacked_widget.addWidget(self.ai_analyser_page)

        self.home_page.request_patients_page.connect(self.go_to_patients)
        self.home_page.menu_patients_statistics_button.clicked.connect(self.go_to_statistics)
        self.home_page.menu_snp_analyser_button.clicked.connect(self.go_to_ai_analyser)
        
        self.patients_page.request_home_page.connect(self.go_to_home)
        self.patients_page.menu_patients_statistics_button.clicked.connect(self.go_to_statistics)
        self.patients_page.menu_snp_analyser_button.clicked.connect(self.go_to_ai_analyser)
        self.patients_page.action_add_patient.connect(self.handle_add_snp)
        self.patients_page.action_delete_patient.connect(self.handle_remove_snp)
        self.patients_page.action_undo.connect(self.handle_undo)
        self.patients_page.action_redo.connect(self.handle_redo)
        self.patients_page.action_search.connect(self.handle_search)
        
        self.statistics_page.request_home_page.connect(self.go_to_home)
        self.statistics_page.request_patients_page.connect(self.go_to_patients)
        if hasattr(self.statistics_page, 'menu_snp_analyser_button'):
            self.statistics_page.menu_snp_analyser_button.clicked.connect(self.go_to_ai_analyser)
        self.statistics_page.action_request_table.connect(self.handle_statistics_table_request)

        self.ai_analyser_page.request_home_page.connect(self.go_to_home)
        self.ai_analyser_page.request_patients_page.connect(self.go_to_patients)
        self.ai_analyser_page.request_statistics_page.connect(self.go_to_statistics)
        self.ai_analyser_page.action_analyse.connect(self.handle_ai_analysis)

        self.stacked_widget.setCurrentWidget(self.home_page)

    def go_to_patients(self):
        self.stacked_widget.setCurrentWidget(self.patients_page)

    def go_to_home(self):
        self.stacked_widget.setCurrentWidget(self.home_page)
        
    def go_to_statistics(self):
        count = self.analyzer_instance.number_of_snps_matching()
        self.statistics_page.update_matching_count_label(count)
        self.stacked_widget.setCurrentWidget(self.statistics_page)

    def go_to_ai_analyser(self):
        self.stacked_widget.setCurrentWidget(self.ai_analyser_page)

    def handle_ai_analysis(self):
        if not self.ai_engine:
            print("AI Engine is not loaded.")
            return

        patient_series = self.analyzer_instance.patients_panel.get_patients_GRPM_RSID()
        
        if patient_series.empty:
            print("No patient data to analyze.")
            return

        patient_rsid_list = patient_series.tolist()
        results, summary, error = self.ai_engine.analyze_patient(patient_rsid_list)

        if error:
            print(f"AI Error: {error}")
            self.ai_analyser_page.operation_error_label.setText(error)
            return

        self.ai_analyser_page.operation_error_label.clear()

        if not hasattr(self.ai_analyser_page, 'overall_score_label'):
            self.ai_analyser_page.overall_score_label = QLabel()
            self.ai_analyser_page.overall_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ai_analyser_page.right_side_widget.layout().insertWidget(1, self.ai_analyser_page.overall_score_label)

        if summary['status'] == "HIGH RISK":
            color = "#a52a2a"
        else:
            color = "#2e8b57"

        summary_text = f"OVERALL RESULT: {summary['status']} | {summary['high_risk_count']}/{summary['total_snps']} Variants Flagged | Average Confidence: {summary['average_confidence']:.1f}%"
        self.ai_analyser_page.overall_score_label.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: white; padding: 10px; border-radius: 4px; margin-bottom: 10px;"
        )
        self.ai_analyser_page.overall_score_label.setText(summary_text)

        model = QStandardItemModel(len(results), 5) 
        model.setHorizontalHeaderLabels(["RSID", "Mapped Trait", "AI Diagnosis", "Confidence", "Odds Ratio"])

        for row_idx, item in enumerate(results):
            rsid_item = QStandardItem(item['rsid'])
            trait_item = QStandardItem(str(item['trait']))
            
            or_value = item['odds_ratio']
            if isinstance(or_value, float):
                or_item = QStandardItem(f"{or_value:.2f}")
            else:
                or_item = QStandardItem(str(or_value))
            
            if item['is_high_risk']:
                diag_item = QStandardItem("HIGH RISK")
                conf_item = QStandardItem(f"{item['confidence']:.1f}%")
                row_color = QColor(80, 20, 20)
            else:
                diag_item = QStandardItem("SAFE")
                conf_item = QStandardItem(f"{item['confidence']:.1f}%")
                row_color = QColor(20, 60, 20)

            diag_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            conf_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            or_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            for col_idx, cell in enumerate((rsid_item, trait_item, diag_item, conf_item, or_item)):
                cell.setBackground(QBrush(row_color))
                cell.setEditable(False)
                model.setItem(row_idx, col_idx, cell)

        table_view = self.ai_analyser_page.patients_analyser_table_view
        table_view.setModel(model)
        
        header = table_view.horizontalHeader()
        header.setStretchLastSection(True)

    def handle_statistics_table_request(self, category):
        df = None
        try:
            if category == "Matching SNPs":
                df = self.analyzer_instance.matching_snps()
            elif category == "MeSH Statistics":
                df = self.analyzer_instance.mesh_statistics()
            elif category == "Shannon Index per SNP":
                df = self.analyzer_instance.shannon_index_per_snp()
            elif category == "Shannon Index per MeSH Term":
                df = self.analyzer_instance.shannon_index_per_mesh()
            
            self.statistics_page.populate_table(df)
        except Exception as e:
            print(f"Statistics Data Error: {e}")

    def handle_add_snp(self, data_string):
        try:
            GRPM_RSID, Chr, Position, EXCG46 = data_string.split('\t')
        except ValueError:
            return
        
        try:
            add_command = add_snp_command.AddSNPCommand(self.analyzer_instance.patients_panel, GRPM_RSID, Chr, Position, EXCG46)
            self.editor.execute_add(GRPM_RSID, Chr, Position, EXCG46)
        except Exception as e:
            print(f"Backend Add Error: {e}")
            return

        self.filtering_patients_instance = filtering_patient_snp.FilteringPatientSNP()
        self.patients_page.trigger_search()

    def handle_remove_snp(self, data_string):
        try:
            GRPM_RSID, Chr, Position, EXCG46 = data_string.split('\t')
        except ValueError:
            return
            
        try:
            remove_command = remove_snp_command.RemoveSNPCommand(self.analyzer_instance.patients_panel, GRPM_RSID, Chr, Position, EXCG46)
            self.editor.execute_remove(GRPM_RSID, Chr, Position, EXCG46)
        except Exception as e:
            print(f"Backend Remove Error: {e}")
            return
            
        self.filtering_patients_instance = filtering_patient_snp.FilteringPatientSNP()
        self.patients_page.trigger_search()
    
    def handle_undo(self):
        try:
            self.editor.undo()
        except Exception as e:
            print(f"Undo Error: {e}")
            
        self.filtering_patients_instance = filtering_patient_snp.FilteringPatientSNP()
        self.patients_page.trigger_search()
    
    def handle_redo(self):
        try:
            self.editor.redo()
        except Exception as e:
            print(f"Redo Error: {e}")
            
        self.filtering_patients_instance = filtering_patient_snp.FilteringPatientSNP()
        self.patients_page.trigger_search()

    def handle_search(self, category, search_term):
        df = None
        try:
            if not search_term:
                self.patients_page.populate_table(None)
                return
            elif category == "rsid":
                df = self.filtering_patients_instance.filter_patients_by_rsid(search_term)
            elif category == "Chr":
                df = self.filtering_patients_instance.filter_patients_by_chr(search_term)
            elif category == "Position":
                df = self.filtering_patients_instance.filter_patients_by_position(search_term)
            elif category == "EXCG46":
                df = self.filtering_patients_instance.filter_patients_by_excg46(search_term)

            self.patients_page.populate_table(df)
        except Exception as e:
            print(f"Search/Filter Error: {e}")

def main():
    app = QApplication(sys.argv)
    
    dark_stylesheet = qdarkstyle.load_stylesheet(qt_api='pyqt6')
    
    app.setStyleSheet(dark_stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()