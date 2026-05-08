import pandas as pd
import os

class GrpmNutrigenRepository:
    def __init__(self):
        data_grpm_nutrigen = pd.read_csv('proj/data/grpm_nutrigen_int_gwas.csv')
        self.grpm_nutrigen = data_grpm_nutrigen

    def get_grpm_nutrigen(self):
        return self.grpm_nutrigen

    def get_grpm_nutrigen_to_string(self):
        return self.grpm_nutrigen.to_string()
    
    def get_grpm_nutrigen_rsid(self):
        return self.grpm_nutrigen['GRPM_RSID']
    
    def group_by_mesh(self):
        return self.grpm_nutrigen.groupby('GRPM_RSID')['GRPM_MESH'].apply(lambda x: ', '.join(set(x.astype(str)))).reset_index()
