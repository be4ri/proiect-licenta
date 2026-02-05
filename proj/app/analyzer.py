import pandas as pd
import os
import app.repository.snp_panel_repository as snp_panel_repository
import app.repository.grpm_nutrigen_repository as grpm_nutrigen_repository
import numpy as np

class Analyzer:
    def __init__(self):
        self.snp_panel_repo = snp_panel_repository.SnpPanelRepository()
        self.grpm_nutrigen_repo = grpm_nutrigen_repository.GrpmNutrigenRepository()

    def number_of_snps_matching(self):
        number_of_matching_snps = self.snp_panel_repo.get_grpm_rsid().isin(self.grpm_nutrigen_repo.get_grpm_nutrigen_rsid()).sum()
        print("Number of matching SNPs:", number_of_matching_snps)
        return number_of_matching_snps
        
    def mesh_statistics(self):
        grpm_nutrigen = self.grpm_nutrigen_repo.grpm_nutrigen
        snp_panel = self.snp_panel_repo.snp_panel
        merged_data = pd.merge(snp_panel[['GRPM_RSID']], grpm_nutrigen[['GRPM_RSID', 'GRPM_MESH']], on='GRPM_RSID', how='inner')
        merged_data = merged_data.drop_duplicates()
        total_snps_with_mesh = merged_data['GRPM_RSID'].nunique()
        mesh_stats = merged_data.groupby('GRPM_MESH').size().reset_index(name='count')
        mesh_stats['proportion'] = mesh_stats['count'] / total_snps_with_mesh
        return mesh_stats.sort_values(by='count', ascending=False)

    def shannon_index_per_snp(self):
        nutrigen_data = self.grpm_nutrigen_repo.grpm_nutrigen
        snp_panel = self.snp_panel_repo.snp_panel
        df = pd.merge(snp_panel[['GRPM_RSID']], nutrigen_data[['GRPM_RSID', 'GRPM_MESH']], on='GRPM_RSID', how='inner')
        counts = df.groupby(['GRPM_RSID', 'GRPM_MESH']).size().reset_index(name='mesh_count')
        total_counts_per_snp = counts.groupby('GRPM_RSID')['mesh_count'].transform('sum')
        counts['p_i'] = counts['mesh_count'] / total_counts_per_snp
        counts['shannon_part'] = counts['p_i'] * np.log(counts['p_i'])
        shannon_index = counts.groupby('GRPM_RSID')['shannon_part'].sum() * -1
        return shannon_index.reset_index(name='shannon_diversity_index')
    
    def shannon_index_per_mesh(self):
        nutrigen_data = self.grpm_nutrigen_repo.grpm_nutrigen
        snp_panel = self.snp_panel_repo.snp_panel
        snp_panel['GRPM_RSID'] = snp_panel['GRPM_RSID'].astype(str).str.strip()
        nutrigen_data['GRPM_RSID'] = nutrigen_data['GRPM_RSID'].astype(str).str.strip()
        df = pd.merge(snp_panel[['GRPM_RSID']], nutrigen_data[['GRPM_RSID', 'GRPM_MESH']], on='GRPM_RSID', how='inner')
        counts = df.groupby(['GRPM_MESH', 'GRPM_RSID']).size().reset_index(name='occurrence_count')
        total_per_mesh = counts.groupby('GRPM_MESH')['occurrence_count'].transform('sum')
        counts['p_i'] = counts['occurrence_count'] / total_per_mesh
        counts['shannon_part'] = counts['p_i'] * np.log(counts['p_i'])
        shannon_index_mesh = counts.groupby('GRPM_MESH')['shannon_part'].sum() * -1
        return shannon_index_mesh.reset_index(name='shannon_diversity_index')