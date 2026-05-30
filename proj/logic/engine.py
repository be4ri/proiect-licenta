import os
import re
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class GenomicEngine:
    def __init__(self, model_rel_path='models/obesity_risk_rf.pkl', db_rel_path='data/encoded_ai_grpm_nutrigen.csv'):
        model_path = os.path.join(BASE_DIR, model_rel_path)
        db_path = os.path.join(BASE_DIR, db_rel_path)
        
        self.rf_model = joblib.load(model_path)
        self.database = pd.read_csv(db_path)

    def _clean_rsid(self, raw_rsid):
        match = re.search(r'(rs\d+)', str(raw_rsid))
        if match:
            return match.group(1)
        return str(raw_rsid)

    def analyze_patient(self, raw_rsid_list):
        cleaned_rsids = [self._clean_rsid(rsid) for rsid in raw_rsid_list]
        patient_data = self.database[self.database['GRPM_RSID'].isin(cleaned_rsids)].copy()
        
        if patient_data.empty:
            return None, None, "None of the entered patient RSIDs match rows in the AI knowledge base."

        expected_features = self.rf_model.feature_names_in_
        
        for feature in expected_features:
            if feature not in patient_data.columns:
                patient_data[feature] = 0
                
        X_patient = patient_data[expected_features]
        predictions = self.rf_model.predict(X_patient)
        probabilities = self.rf_model.predict_proba(X_patient)[:, 1]

        results = []
        high_risk_count = 0

        for i in range(len(patient_data)):
            odds_ratio_val = patient_data.iloc[i].get('GWAS_OR-BETA', 'N/A')
            is_high = bool(predictions[i] == 1)
            
            if is_high:
                high_risk_count += 1

            results.append({
                'rsid': patient_data.iloc[i]['GRPM_RSID'],
                'trait': patient_data.iloc[i]['GWAS_MAPPED_TRAIT'] if 'GWAS_MAPPED_TRAIT' in patient_data.columns else "Unknown Trait",
                'is_high_risk': is_high,
                'confidence': float(probabilities[i] * 100),
                'odds_ratio': odds_ratio_val
            })
            
        total_snps = len(results)
        avg_confidence = sum(r['confidence'] for r in results) / total_snps if total_snps > 0 else 0
        overall_is_high_risk = (high_risk_count / total_snps) >= 0.5
        
        summary = {
            'status': 'HIGH RISK' if overall_is_high_risk else 'SAFE',
            'high_risk_count': high_risk_count,
            'total_snps': total_snps,
            'average_confidence': avg_confidence
        }

        return results, summary, None