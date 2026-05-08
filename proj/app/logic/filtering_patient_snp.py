import re
import pandas as pd

from repository.patients_repository import PatientsRepository

class FilteringPatientSNP:
    def __init__(self):
        self.patients_repo = PatientsRepository()

    def filter_patients_by_snp(self, rsid):
        return self.patients_repo.filter_by_rsid(rsid)
    
    def filter_patients_by_chr(self, chr_val):
        return self.patients_repo.filter_by_chr(chr_val)
    
    def filter_patients_by_position(self, position):
        return self.patients_repo.filter_by_position(position)
    
    def filter_patients_by_excg46(self, excg46):
        return self.patients_repo.filter_by_excg46(excg46)
    
