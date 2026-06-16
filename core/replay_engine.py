"""
==========================================================
QuantEdge AI
Historical Replay Engine
==========================================================
"""
import pandas as pd
from datetime import datetime

class ReplayEngine:
    def __init__(self, provider, pipeline, paper_broker, start_date, end_date, resolution_minutes=5):
        self.provider = provider
        self.pipeline = pipeline
        self.broker = paper_broker
        
        self.timestamps = pd.date_range(start=start_date, end=end_date, freq=f'{resolution_minutes}min')
        
        # Filter for Indian market hours (09:15 to 15:30)
        start_time = datetime.strptime("09:15", "%H:%M").time()
        end_time = datetime.strptime("15:30", "%H:%M").time()
        self.timestamps = [ts for ts in self.timestamps if ts.weekday() < 5 and start_time <= ts.time() <= end_time]
        
    def run(self):
        total_steps = len(self.timestamps)
        
        for i, ts in enumerate(self.timestamps):
            print(f"[{i+1}/{total_steps}] Replaying {ts} ...")
            
            # 1. Abstract time bounds
            self.provider.set_timestamp(ts)
            
            # 2. Mark-to-Market & Exit Evaluation
            open_pos = self.broker.positions()
            current_quotes = {}
            for option_symbol in open_pos.keys():
                q = self.provider.quote(option_symbol)
                if q and 'd' in q and len(q['d']) > 0:
                    current_quotes[option_symbol] = q['d'][0]['v']['lp']
            
            is_data_end = (i == total_steps - 1)
            self.broker.evaluate_exits(current_time=ts, quotes_dict=current_quotes, is_data_end=is_data_end)
            
            # 3. Entry Pipeline Execution
            cutoff_time = datetime.strptime("15:15", "%H:%M").time()
            if ts.time() < cutoff_time and not is_data_end:
                # 30-day historical window for indicators
                hist_start = (ts - pd.Timedelta(days=30)).strftime("%Y-%m-%d")
                
                try:
                    result = self.pipeline.run(resolution="5", start=hist_start, end=ts.strftime("%Y-%m-%d %H:%M:%S"))
                    decision = result.get("decision")
                    if decision and getattr(decision, "action", "") == "EXECUTE":
                        # Prevent duplicate entries on the same day for the same symbol
                        # (Basic portfolio constraint to prevent taking the exact same trade every 5 mins)
                        existing_open = self.broker.positions()
                        if not any(pos.symbol == decision.candidate.symbol for pos in existing_open.values()):
                            self.broker.execute_decision(decision, current_time=ts)
                except Exception as e:
                    print(f"Pipeline error at {ts}: {e}")
                    
        print("Backtest Replay Complete.")
