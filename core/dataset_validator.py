"""
==========================================================
QuantEdge AI
Dataset Validator
==========================================================
"""
import pandas as pd
import json

class DatasetValidator:
    def __init__(self, underlying_path, options_path):
        self.underlying_path = underlying_path
        self.options_path = options_path
        
    def run_validation(self):
        try:
            udf = pd.read_csv(self.underlying_path)
            odf = pd.read_csv(self.options_path)
        except Exception as e:
            return {"Error": f"Failed to load datasets: {e}"}
            
        report = {
            "Underlying_Rows": len(udf),
            "Options_Rows": len(odf),
            "Duplicate_Underlying_Rows": int(udf.duplicated().sum()),
            "Duplicate_Options_Rows": int(odf.duplicated().sum()),
            "Chronology_Violations": 0,
            "Missing_CE": 0,
            "Missing_PE": 0,
            "Missing_Bid": int(odf['Bid'].isnull().sum()),
            "Missing_Ask": int(odf['Ask'].isnull().sum()),
            "Missing_OI": int(odf['OI'].isnull().sum()),
            "Negative_OI": int((odf['OI'] < 0).sum()),
            "Negative_Volume": int((odf['Volume'] < 0).sum()),
            "Negative_Bid": int((odf['Bid'] < 0).sum()),
            "Negative_Ask": int((odf['Ask'] < 0).sum()),
            "Spread_Violations": int((odf['Ask'] < odf['Bid']).sum()),
            "Missing_Expiry": int(odf['Expiry'].isnull().sum())
        }
        
        # Check chronology
        udf['Datetime'] = pd.to_datetime(udf['Datetime'])
        if not udf['Datetime'].is_monotonic_increasing:
            report['Chronology_Violations'] += 1
            
        odf['Datetime'] = pd.to_datetime(odf['Datetime'])
        if not odf['Datetime'].is_monotonic_increasing:
            report['Chronology_Violations'] += 1
            
        # Group by datetime to check CE/PE presence
        for dt, group in odf.groupby('Datetime'):
            types = group['OptionType'].unique()
            if 'CE' not in types:
                report['Missing_CE'] += 1
            if 'PE' not in types:
                report['Missing_PE'] += 1
                
        # Calculate Health Score
        total_checks = report['Underlying_Rows'] + report['Options_Rows']
        violations = (
            report['Duplicate_Underlying_Rows'] +
            report['Duplicate_Options_Rows'] +
            report['Chronology_Violations'] * 100 +
            report['Missing_CE'] +
            report['Missing_PE'] +
            report['Missing_Bid'] +
            report['Missing_Ask'] +
            report['Missing_OI'] +
            report['Negative_OI'] +
            report['Negative_Volume'] +
            report['Negative_Bid'] +
            report['Negative_Ask'] +
            report['Spread_Violations'] +
            report['Missing_Expiry']
        )
        
        if total_checks > 0:
            score = max(0.0, 100.0 * (1.0 - (violations / total_checks)))
        else:
            score = 0.0
            
        report['Dataset_Health_Score'] = round(score, 2)
        report['Status'] = "PASS" if score > 95.0 else "FAIL"
        
        return report
        
    def export(self, filepath):
        import os
        report = self.run_validation()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=4)
        return report

if __name__ == "__main__":
    validator = DatasetValidator("data/historical/underlying.csv", "data/historical/options.csv")
    rep = validator.export("analysis/metrics/dataset_health_report.json")
    print(f"Dataset Health Score: {rep.get('Dataset_Health_Score', 0)}% - {rep.get('Status', 'FAIL')}")
