import re
import pandas as pd

class RemoveSNPCommand:
    def __init__(self, repository, rsid, chr_val, pos, excg):
        self.repository = repository
        self.data = (rsid, chr_val, pos, excg)

    def execute(self):
        self.repository.remove_SNP_from_csv_file(*self.data)

    def undo(self):
        self.repository.add_SNP_to_csv_file(*self.data)