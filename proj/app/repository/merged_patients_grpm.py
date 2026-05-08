import pandas as pd
import app.repository.grpm_nutrigen_repository as grpm_nutrigen_repository
import app.repository.patients_repository as patients_repository
import app.repository.rs_repository as rs_repository

class MergedPatientsGrpm:
    def __init__(self):
        self.grpm_panel = grpm_nutrigen_repository.GrpmNutrigenRepository().get_grpm_nutrigen()
        self.patients_panel = patients_repository.PatientsRepository().get_patients()
        self.rs_panel = rs_repository.RSRepository().get_rs_panel()

    def get_patients_rsid(self):
        self.rs_panel['Chr'] = self.rs_panel['Chr'].astype(str).str.replace('chr', '', case=False)
        self.patients_panel['Chr'] = self.patients_panel['Chr'].astype(str)
        merge_patients_rs = pd.merge(self.patients_panel, self.rs_panel[['Chr', 'Position', 'rsid']], left_on=['Chr', 'Position'], 
            right_on=['Chr', 'Position'], how='left')
        return merge_patients_rs
    
    def create_csv_file_patients_rsid(self):
        merge_patients_rs = self.get_patients_rsid()
        merge_patients_rs.to_csv('proj/data/merged_patients_rs.csv', index=False)

    def get_merged_patients_grpm_nutrigen(self):
        merge_patients_grpm_on_rsid = pd.merge(self.patients_panel[['GRPM_RSID']], self.grpm_panel[['GRPM_RSID']], left_on='GRPM_RSID', right_on='GRPM_RSID', how='inner')
        return merge_patients_grpm_on_rsid

    def create_csv_file_merged_patients_grpm_nutrigen(self):
        merge_patients_grpm_on_rsid = self.get_merged_patients_grpm_nutrigen()
        merge_patients_grpm_on_rsid.to_csv('proj/data/merged_patients_grpm_nutrigen.csv', index=False)