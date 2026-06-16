"""
==========================================================
QuantEdge AI
Statistics Engine
==========================================================
"""
import pandas as pd
import numpy as np

class StatisticsEngine:
    def __init__(self, ledger_df):
        # We expect a DataFrame from TradeLedger.export()
        self.df = ledger_df
        
    def compute(self):
        if self.df.empty:
            return {"Error": "No trades executed."}
            
        stats = {}
        
        # Base Data
        pnl = self.df['PnL'].values
        wins = pnl[pnl > 0]
        losses = pnl[pnl <= 0]
        
        # 1. Trade Statistics
        stats['Total Trades'] = len(self.df)
        stats['Winners'] = len(wins)
        stats['Losers'] = len(losses)
        stats['Win Rate'] = len(wins) / len(self.df) if len(self.df) > 0 else 0
        stats['Loss Rate'] = 1.0 - stats['Win Rate']
        
        # 2. Return Statistics
        stats['Average Win'] = np.mean(wins) if len(wins) > 0 else 0
        stats['Average Loss'] = np.mean(losses) if len(losses) > 0 else 0
        stats['Median Win'] = np.median(wins) if len(wins) > 0 else 0
        stats['Median Loss'] = np.median(losses) if len(losses) > 0 else 0
        
        gross_profit = np.sum(wins) if len(wins) > 0 else 0
        gross_loss = np.abs(np.sum(losses)) if len(losses) > 0 else 0
        stats['Profit Factor'] = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
        
        stats['Expectancy'] = (stats['Win Rate'] * stats['Average Win']) + (stats['Loss Rate'] * stats['Average Loss'])
        
        # 3. Risk Statistics
        cum_pnl = np.cumsum(pnl)
        running_max = np.maximum.accumulate(cum_pnl)
        drawdowns = running_max - cum_pnl
        stats['Max Drawdown'] = np.max(drawdowns) if len(drawdowns) > 0 else 0
        
        # Consecutive wins/losses
        is_win = (pnl > 0).astype(int)
        is_loss = (pnl <= 0).astype(int)
        
        def max_consecutive(arr):
            max_c = 0
            curr_c = 0
            for val in arr:
                if val == 1:
                    curr_c += 1
                    max_c = max(max_c, curr_c)
                else:
                    curr_c = 0
            return max_c
            
        stats['Max Consecutive Wins'] = max_consecutive(is_win)
        stats['Max Consecutive Losses'] = max_consecutive(is_loss)
        
        # 4. Portfolio Statistics
        total_pnl = np.sum(pnl)
        stats['Total PnL'] = total_pnl
        # Assuming initial capital 100k
        initial_cap = 100000.0
        final_cap = initial_cap + total_pnl
        
        # CAGR (assuming daily data timeframe, we approximate from timestamps)
        if 'entry' in self.df.columns and not self.df['entry'].isnull().all():
            start_date = pd.to_datetime(self.df['entry'].iloc[0])
            end_date = pd.to_datetime(self.df['entry'].iloc[-1])
            days = (end_date - start_date).days
            if days > 0:
                years = days / 365.25
                stats['CAGR'] = ((final_cap / initial_cap) ** (1/years)) - 1 if years > 0 else 0
            else:
                stats['CAGR'] = 0.0
        else:
            stats['CAGR'] = 0.0
            
        # Approximation for Sharpe/Sortino on trade sequence
        if len(pnl) > 1:
            mean_pnl = np.mean(pnl)
            std_pnl = np.std(pnl)
            stats['Sharpe Ratio'] = (mean_pnl / std_pnl) * np.sqrt(252) if std_pnl > 0 else 0
            
            downside_dev = np.std(losses) if len(losses) > 1 else 0
            stats['Sortino Ratio'] = (mean_pnl / downside_dev) * np.sqrt(252) if downside_dev > 0 else 0
        else:
            stats['Sharpe Ratio'] = 0
            stats['Sortino Ratio'] = 0
            
        stats['Recovery Factor'] = total_pnl / stats['Max Drawdown'] if stats['Max Drawdown'] > 0 else float('inf')
        
        # 5. Calibration Statistics
        if 'PredictionError' in self.df.columns:
            stats['Mean Prediction Error'] = self.df['PredictionError'].mean()
            stats['Median Prediction Error'] = self.df['PredictionError'].median()
            
        return stats

    def export_reports(self, output_dir, benchmark_df=None, manifest_kwargs=None):
        import os
        import json
        import pandas as pd
        import numpy as np
        from datetime import datetime
        import subprocess
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Summary with version stamping
        stats = self.compute()
        
        git_commit = "unknown"
        try:
            git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        except Exception:
            pass
        
        report_meta = {
            "git_commit": git_commit,
            "strategy_version": manifest_kwargs.get("strategy_version", "QuantEdge_v1.0") if manifest_kwargs else "QuantEdge_v1.0",
            "report_generated": datetime.now().isoformat(),
            "dataset": manifest_kwargs.get("dataset_name", "unknown") if manifest_kwargs else "unknown",
            "trade_count": len(self.df)
        }
        
        stats.update(report_meta)
        
        with open(os.path.join(output_dir, "summary.json"), 'w') as f:
            json.dump(stats, f, indent=4)
            
        # 1b. Research Manifest
        if manifest_kwargs:
            manifest = {
                "git_commit": git_commit,
                "strategy_version": manifest_kwargs.get("strategy_version", "QuantEdge_v1.0"),
                "dataset_name": manifest_kwargs.get("dataset_name", "unknown"),
                "dataset_start": manifest_kwargs.get("dataset_start", "unknown"),
                "dataset_end": manifest_kwargs.get("dataset_end", "unknown"),
                "trade_count": len(self.df),
                "symbols": manifest_kwargs.get("symbols", []),
                "resolution": manifest_kwargs.get("resolution", "5m")
            }
            with open(os.path.join(output_dir, "research_manifest.json"), 'w') as f:
                json.dump(manifest, f, indent=4)
                
        if self.df.empty:
            return
            
        # Ensure Datetimes
        if 'entry' in self.df.columns:
            self.df['entry'] = pd.to_datetime(self.df['entry'])
            
        # 2. Monthly Returns
        if 'entry' in self.df.columns:
            self.df['MonthYear'] = self.df['entry'].dt.to_period('M')
            monthly = self.df.groupby('MonthYear').agg(
                Trades=('PnL', 'count'),
                PnL=('PnL', 'sum'),
                WinRate=('PnL', lambda x: (x > 0).mean()),
                Expectancy=('PnL', 'mean')
            ).reset_index()
            monthly['MonthYear'] = monthly['MonthYear'].astype(str)
            monthly.to_csv(os.path.join(output_dir, "monthly_returns.csv"), index=False)
            
        # 3. Drawdowns
        pnl = self.df['PnL'].values
        cum_pnl = np.cumsum(pnl)
        running_max = np.maximum.accumulate(cum_pnl)
        drawdowns = running_max - cum_pnl
        dd_df = pd.DataFrame({"TradeIndex": range(len(drawdowns)), "Drawdown": drawdowns})
        if 'entry' in self.df.columns:
            dd_df['Date'] = self.df['entry']
        dd_df.to_csv(os.path.join(output_dir, "drawdowns.csv"), index=False)
        
        # 4. Probability Calibration
        if 'Prob' in self.df.columns:
            df_prob = self.df.copy()
            df_prob['Observed_Win'] = (df_prob['PnL'] > 0).astype(int)
            bins = np.linspace(0, 1, 11)
            df_prob['Bin'] = pd.cut(df_prob['Prob'], bins=bins)
            
            calib = df_prob.groupby('Bin', observed=False).agg(
                TradeCount=('Observed_Win', 'count'),
                Predicted=('Prob', 'mean'),
                Observed=('Observed_Win', 'mean')
            ).reset_index()
            
            # Brier Score = 1/N * sum((pred - obs_win)^2)
            brier_score = np.mean((df_prob['Prob'] - df_prob['Observed_Win'])**2)
            
            # ECE = sum(|pred_bin - obs_bin| * bin_count) / N
            total_trades = len(df_prob)
            ece = np.sum(np.abs(calib['Predicted'].fillna(0) - calib['Observed'].fillna(0)) * calib['TradeCount']) / total_trades if total_trades > 0 else 0
            
            calib['BrierScore'] = brier_score
            calib['CalibrationError'] = ece
            calib['Bin'] = calib['Bin'].astype(str)
            calib.to_csv(os.path.join(output_dir, "probability_calibration.csv"), index=False)
            
        # 5. Benchmark Comparison
        if benchmark_df is not None and not benchmark_df.empty and 'entry' in self.df.columns:
            # Placeholder for proper join logic
            pass
        else:
            # Fallback
            pd.DataFrame({"Date": [], "StrategyReturn": [], "BenchmarkReturn": [], "Alpha": [], "ExcessReturn": []}).to_csv(os.path.join(output_dir, "benchmark_comparison.csv"), index=False)
            
        # 6. Trade Distribution
        bins_dist = np.histogram_bin_edges(pnl, bins=20)
        hist, edges = np.histogram(pnl, bins=bins_dist)
        dist_df = pd.DataFrame({"BinStart": edges[:-1], "BinEnd": edges[1:], "Count": hist})
        dist_df.to_csv(os.path.join(output_dir, "trade_distribution.csv"), index=False)
        
        # 7. Equity Curve CSV
        equity_df = pd.DataFrame()
        if 'entry' in self.df.columns:
            equity_df['timestamp'] = self.df['entry']
        else:
            equity_df['timestamp'] = range(len(self.df))
            
        equity_df['equity'] = cum_pnl
        equity_df['drawdown'] = drawdowns
        
        rolling_mean = self.df['PnL'].rolling(20).mean()
        rolling_std = self.df['PnL'].rolling(20).std()
        equity_df['rolling_sharpe'] = (rolling_mean / rolling_std) * np.sqrt(252)
        
        equity_df.to_csv(os.path.join(output_dir, "equity_curve.csv"), index=False)

    def generate_charts(self, output_dir):
        import os
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        
        os.makedirs(output_dir, exist_ok=True)
        
        if self.df.empty:
            return
            
        pnl = self.df['PnL'].values
        cum_pnl = np.cumsum(pnl)
        running_max = np.maximum.accumulate(cum_pnl)
        drawdowns = running_max - cum_pnl
        
        x_axis = range(len(cum_pnl))
        if 'entry' in self.df.columns:
            try:
                x_axis = pd.to_datetime(self.df['entry'])
            except:
                pass
                
        # 1. Equity Curve
        plt.figure(figsize=(10, 5))
        plt.plot(x_axis, cum_pnl, label='Cumulative PnL', color='blue')
        plt.title('Equity Curve')
        plt.xlabel('Trades')
        plt.ylabel('PnL')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "equity_curve.png"))
        plt.close()
        
        # 2. Drawdown Curve
        plt.figure(figsize=(10, 5))
        plt.fill_between(x_axis, -drawdowns, 0, color='red', alpha=0.5, label='Drawdown')
        plt.title('Drawdown Curve')
        plt.xlabel('Trades')
        plt.ylabel('Drawdown')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "drawdown_curve.png"))
        plt.close()
        
        # 3. Calibration Curve
        if 'Prob' in self.df.columns:
            df_prob = self.df.copy()
            df_prob['Observed_Win'] = (df_prob['PnL'] > 0).astype(int)
            bins = np.linspace(0, 1, 11)
            df_prob['Bin'] = pd.cut(df_prob['Prob'], bins=bins)
            calib = df_prob.groupby('Bin', observed=False).agg(
                Predicted=('Prob', 'mean'),
                Observed=('Observed_Win', 'mean'),
                Count=('Observed_Win', 'count')
            ).dropna()
            
            plt.figure(figsize=(8, 8))
            plt.plot([0, 1], [0, 1], 'k--', label='Perfect Calibration')
            if not calib.empty:
                plt.scatter(calib['Predicted'], calib['Observed'], s=calib['Count']*10, alpha=0.7, color='purple', label='Binned Observations')
                plt.plot(calib['Predicted'], calib['Observed'], color='purple', alpha=0.5)
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            plt.title('Probability Calibration')
            plt.xlabel('Predicted Probability')
            plt.ylabel('Observed Win Rate')
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "calibration_curve.png"))
            plt.close()
            
        # 4. Monthly Heatmap
        if 'entry' in self.df.columns:
            try:
                df_hm = self.df.copy()
                df_hm['entry'] = pd.to_datetime(df_hm['entry'])
                df_hm['Year'] = df_hm['entry'].dt.year
                df_hm['Month'] = df_hm['entry'].dt.month
                pivot = df_hm.pivot_table(values='PnL', index='Year', columns='Month', aggfunc='sum')
                
                plt.figure(figsize=(10, 6))
                plt.imshow(pivot, cmap='RdYlGn', aspect='auto')
                plt.colorbar(label='PnL')
                plt.title('Monthly Returns Heatmap')
                plt.xticks(ticks=np.arange(len(pivot.columns)), labels=pivot.columns)
                plt.yticks(ticks=np.arange(len(pivot.index)), labels=pivot.index)
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, "monthly_heatmap.png"))
                plt.close()
            except Exception as e:
                pass
