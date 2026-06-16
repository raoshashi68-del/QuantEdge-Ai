"""
==========================================================
QuantEdge AI
Historical Data Provider
==========================================================
"""
import pandas as pd
from interfaces.data_provider import DataProvider

class HistoricalDataProvider(DataProvider):
    def __init__(self, underlying_path, options_path):
        self.current_time = None
        
        # Load datasets
        self.underlying_df = pd.read_csv(underlying_path, parse_dates=['Datetime'])
        self.options_df = pd.read_csv(options_path, parse_dates=['Datetime'])
        
        # Sort chronologically to guarantee correct point-in-time slicing
        self.underlying_df.sort_values('Datetime', inplace=True)
        self.options_df.sort_values('Datetime', inplace=True)
        
    def set_timestamp(self, current_time):
        self.current_time = pd.to_datetime(current_time)
        # Precompute indices using searchsorted
        self.underlying_idx = self.underlying_df['Datetime'].searchsorted(self.current_time, side='right')
        self.options_idx = self.options_df['Datetime'].searchsorted(self.current_time, side='right')
        
    def history(self, symbol, resolution, start, end):
        if not self.current_time:
            raise ValueError("Internal timestamp not set in HistoricalDataProvider")
            
        safe_end = min(pd.to_datetime(end), self.current_time)
        start_dt = pd.to_datetime(start)
        
        # Use iloc slice to guarantee no forward-looking bias
        view = self.underlying_df.iloc[:self.underlying_idx]
        
        mask = (
            (view['Symbol'] == symbol) &
            (view['Datetime'] >= start_dt) &
            (view['Datetime'] <= safe_end)
        )
        
        df = view[mask].copy()
        if df.empty:
            return None
            
        return df

    def quote(self, symbol):
        if not self.current_time:
            return None
            
        if len(symbol) > 10 and ("C" in symbol or "P" in symbol):
            view = self.options_df.iloc[:self.options_idx]
            mask = (view['OptionSymbol'] == symbol)
            df = view[mask]
            if df.empty:
                return None
            last_row = df.iloc[-1]
            return {"s": "ok", "d": [{"v": {"lp": last_row['LTP'], "bid": last_row['Bid'], "ask": last_row['Ask']}}]}
        else:
            view = self.underlying_df.iloc[:self.underlying_idx]
            mask = (view['Symbol'] == symbol)
            df = view[mask]
            if df.empty:
                return None
            last_row = df.iloc[-1]
            return {"s": "ok", "d": [{"v": {"lp": last_row['Close']}}]}

    def option_chain(self, symbol):
        if not self.current_time:
            return []
            
        view = self.options_df.iloc[:self.options_idx]
        mask = (view['Symbol'] == symbol)
        df = view[mask]
        
        if df.empty:
            return []
            
        latest = df.sort_values('Datetime').groupby('OptionSymbol').last().reset_index()
        
        chain = []
        for _, row in latest.iterrows():
            chain.append({
                "symbol": row['OptionSymbol'],
                "option_type": row['OptionType'],
                "strike_price": row['Strike'],
                "ltp": row['LTP'],
                "volume": row['Volume'],
                "oi": row['OI'],
                "bid": row['Bid'],
                "ask": row['Ask'],
                "expiry": str(row.get('Expiry', ''))
            })
            
        return chain
