import pandas as pd

class PatientsRepository:
    def __init__(self):
        data_patients =pd.read_csv('proj/data/patients.csv', names=['GRPM_RSID', 'Chr', 'Position', 'EXCG46'], sep='\t',dtype={'Chr': str, 'Position': str},low_memory=False)
        self.patients = data_patients
        self.file_path = 'proj/data/patients.csv'

    def get_patients(self):
        return self.patients
    
    def get_patients_GRPM_RSID(self):
        return self.patients['GRPM_RSID']
    
    def add_SNP_to_csv_file(self, GRPM_RSID, Chr, Position, EXCG46):
        new_row = pd.DataFrame([
            [GRPM_RSID], 
            [Chr], 
            [Position], 
            [EXCG46]
        ])
        self.patients = pd.concat([self.patients, new_row], ignore_index=True)
        self._save_to_csv()

    def remove_SNP_from_csv_file(self, GRPM_RSID, Chr, Position, EXCG46):

        exact_match = (
            (self.patients['GRPM_RSID'] == GRPM_RSID) & 
            (self.patients['Chr'] == Chr) & 
            (self.patients['Position'] == Position) & 
            (self.patients['EXCG46'] == EXCG46)
        )
        self.patients = self.patients[~exact_match]
        self._save_to_csv()

    def _save_to_csv(self):
        self.patients.to_csv(self.file_path, index=False, sep='\t', header=True)

    def filter_by_rsid(self, rsid):
        return self.patients[self.patients['GRPM_RSID'] == rsid]
    
    def filter_by_chr(self, Chr):
        return self.patients[(self.patients['Chr'] == Chr)]
    
    def filter_by_position(self, Position):
        return self.patients[self.patients['Position'] == Position]
    
    def filter_by_excg46(self, excg46):
        return self.patients[self.patients['EXCG46'] == excg46]