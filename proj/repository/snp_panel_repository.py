import pandas as pd
import os

class SnpPanelRepository:
    def __init__(self):
        data_snp_panel = pd.read_csv('proj/data/snp_panel.csv')
        self.snp_panel = data_snp_panel
    
    def get_snp_panel(self):
        return self.snp_panel.to_string()
    
    def get_grpm_rsid(self):
        return self.snp_panel['GRPM_RSID']