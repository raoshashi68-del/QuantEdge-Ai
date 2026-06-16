"""
==========================================================
QuantEdge AI
Trade Ledger
==========================================================
"""
import pandas as pd
import os

class TradeLedger:
    def __init__(self):
        self.positions = []
        
    def append(self, position):
        self.positions.append(position)
        
    def retrieve(self):
        return self.positions
        
    def filter(self, **kwargs):
        filtered = self.positions
        for key, value in kwargs.items():
            filtered = [p for p in filtered if getattr(p, key, None) == value]
        return filtered
        
    def export(self, filepath):
        data = []
        for p in self.positions:
            ev = p.expected_value_result.expected_value if getattr(p, 'expected_value_result', None) else 0.0
            prob = p.probability_result.probability if getattr(p, 'probability_result', None) else 0.0
            conf = p.confidence_result.confidence if getattr(p, 'confidence_result', None) else 0.0
            exp_ret = p.expected_return_result.expected_return if getattr(p, 'expected_return_result', None) else 0.0
            exp_loss = p.risk_result.expected_loss if getattr(p, 'risk_result', None) else 0.0
            
            row = {
                "trade_id": getattr(p, 'trade_id', ''),
                "symbol": getattr(p, 'symbol', ''),
                "entry": p.entry_time.isoformat() if getattr(p, 'entry_time', None) else "",
                "exit": p.exit_time.isoformat() if getattr(p, 'exit_time', None) else "",
                "EV": ev,
                "Prob": prob,
                "Conf": conf,
                "ExpectedReturn": exp_ret,
                "ExpectedLoss": exp_loss,
                "PnL": getattr(p, 'pnl', 0.0),
                "PredictionError": getattr(p, 'prediction_error', 0.0),
                "ExitReason": getattr(p, 'exit_reason', '') or ""
            }
            data.append(row)
            
        df = pd.DataFrame(data)
        if df.empty:
            df = pd.DataFrame(columns=["trade_id", "symbol", "entry", "exit", "EV", "Prob", "Conf", "ExpectedReturn", "ExpectedLoss", "PnL", "PredictionError", "ExitReason"])
            
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        df.to_csv(filepath, index=False)
        return True
        
    def export_attribution(self, filepath):
        data = []
        for p in self.positions:
            row = {"trade_id": getattr(p, 'trade_id', '')}
            
            if hasattr(p, 'evidence') and p.evidence and hasattr(p.evidence, 'features'):
                features = p.evidence.features
                row['trend'] = features.get('trend', 0.0)
                row['momentum'] = features.get('momentum', 0.0)
                row['volume'] = features.get('volume', 0.0)
                row['volatility'] = features.get('volatility', 0.0)
                row['structure'] = features.get('structure', 0.0)
                row['execution'] = features.get('execution', 0.0)
                row['consistency'] = features.get('consistency', 0.0)
            else:
                row['trend'] = row['momentum'] = row['volume'] = row['volatility'] = 0.0
                row['structure'] = row['execution'] = row['consistency'] = 0.0
                
            row['probability'] = p.probability_result.probability if getattr(p, 'probability_result', None) else 0.0
            row['expected_return'] = p.expected_return_result.expected_return if getattr(p, 'expected_return_result', None) else 0.0
            row['expected_loss'] = p.risk_result.expected_loss if getattr(p, 'risk_result', None) else 0.0
            row['expected_value'] = p.expected_value_result.expected_value if getattr(p, 'expected_value_result', None) else 0.0
            
            row['realized_return'] = getattr(p, 'realized_return', 0.0)
            row['pnl'] = getattr(p, 'pnl', 0.0)
            data.append(row)
            
        df = pd.DataFrame(data)
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        df.to_csv(filepath, index=False)
        return True
