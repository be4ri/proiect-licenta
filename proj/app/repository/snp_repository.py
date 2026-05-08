import pandas as pd
import requests 

class SnpRepository:
    def __init__(self):
        self.snp_panel = pd.read_csv('proj/data/snp_dataset.csv')
    
    