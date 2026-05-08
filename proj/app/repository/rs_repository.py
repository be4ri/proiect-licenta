import pandas as pd

class RSRepository:
    def __init__(self):
        data_rs = pd.read_csv('proj/data/rs_file.csv', names=['Chr', 'Start', 'Position', 'rsid'], sep='\t')
        self.rs_panel = data_rs
    
    def get_rs_panel(self):
        return self.rs_panel
