"""
==========================================================
QuantEdge AI
Backtest Entry Point
==========================================================
"""
import os
import pandas as pd

from core.universe_manager import UniverseManager
from providers.historical_provider import HistoricalDataProvider
from paper_trading.paper_broker import PaperBroker
from engines.data_engine import DataEngine
from engines.feature_engine import FeatureEngine
from engines.option_chain_parser import OptionChainParser
from engines.strike_selector import StrikeSelector
from engines.candidate_engine import CandidateEngine
from engines.filter_engine import FilterEngine
from engines.evidence_engine import EvidenceEngine
from engines.probability_engine import ProbabilityEngine
from engines.expected_return_engine import ExpectedReturnEngine
from engines.risk_engine import RiskEngine
from engines.expected_value_engine import ExpectedValueEngine
from engines.confidence_engine import ConfidenceEngine
from engines.ranking_engine import RankingEngine
from engines.decision_engine import DecisionEngine
from core.live_scan_pipeline import LiveScanPipeline
from core.replay_engine import ReplayEngine
from paper_trading.statistics_engine import StatisticsEngine

def main():
    print("Initializing QuantEdge Historical Backtest Framework...")
    
    # 1. Directories
    os.makedirs("analysis/ledgers", exist_ok=True)
    os.makedirs("analysis/reports", exist_ok=True)
    
    # 2. Universe
    universe = UniverseManager()
    universe.add_many(["RELIANCE"])
    
    # 3. Provider
    underlying_path = "data/historical/underlying.csv"
    options_path = "data/historical/options.csv"
    if not os.path.exists(underlying_path) or not os.path.exists(options_path):
        print(f"Error: Historical data missing at data/historical/.")
        return
        
    historical_provider = HistoricalDataProvider(underlying_path, options_path)
    
    # 4. Broker & Pipeline
    paper_broker = PaperBroker(market_data_provider=historical_provider, initial_capital=100000)
    data_engine = DataEngine(broker=paper_broker)
    
    pipeline = LiveScanPipeline(
        universe_manager=universe,
        data_engine=data_engine,
        feature_engine=FeatureEngine(),
        option_chain_parser=OptionChainParser(),
        strike_selector=StrikeSelector(),
        candidate_engine=CandidateEngine(),
        filter_engine=FilterEngine(),
        ranking_engine=RankingEngine(),
        decision_engine=DecisionEngine(),
        evidence_engine=EvidenceEngine(),
        probability_engine=ProbabilityEngine(),
        expected_return_engine=ExpectedReturnEngine(),
        risk_engine=RiskEngine(),
        expected_value_engine=ExpectedValueEngine(),
        confidence_engine=ConfidenceEngine()
    )
    
    # 5. Replay Engine
    start_date = "2026-06-01 09:15:00"
    end_date = "2026-06-01 15:30:00"
    
    replay = ReplayEngine(
        provider=historical_provider,
        pipeline=pipeline,
        paper_broker=paper_broker,
        start_date=start_date,
        end_date=end_date,
        resolution_minutes=5
    )
    
    print("\nStarting Replay...")
    
    # Suppress verbose prints from pipeline to keep backtest logs clean
    import sys
    import io
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        replay.run()
    except Exception as e:
        sys.stdout = original_stdout
        print(f"\nReplay Failed: {e}")
        import traceback
        traceback.print_exc()
        return
        
    sys.stdout = original_stdout
    
    print("Replay Engine Completed.")
    
    # 6. Export Ledger & Statistics
    ledger_path = "analysis/ledgers/backtest_ledger.csv"
    paper_broker.ledger.export(ledger_path)
    print(f"Exported Ledger to {ledger_path}")
    
    ledger_df = pd.read_csv(ledger_path)
    stats_engine = StatisticsEngine(ledger_df)
    
    report_path = "analysis/reports/summary.json"
    stats_engine.export_reports("analysis/reports", manifest_kwargs={
        "strategy_version": "QuantEdge_v1.0",
        "dataset_name": "historical_replay_1",
        "dataset_start": "Unknown",
        "dataset_end": "Unknown",
        "symbols": ["RELIANCE"],
        "resolution": "5m"
    })
    stats_engine.generate_charts("analysis/charts")
    paper_broker.ledger.export_attribution("analysis/reports/feature_attribution.csv")
    print(f"Exported Statistics and Charts to analysis/reports and analysis/charts")
    
    # Print high level stats
    stats = stats_engine.compute()
    print("\n===============================")
    print("BACKTEST RESULTS (P2 Snapshot)")
    print("===============================")
    print(f"Total Trades: {stats.get('Total Trades', 0)}")
    print(f"Win Rate:     {stats.get('Win Rate', 0):.2%}")
    print(f"Profit Factor:{stats.get('Profit Factor', 0):.2f}")
    print(f"Expectancy:   {stats.get('Expectancy', 0):.2f}")
    print(f"Max Drawdown: {stats.get('Max Drawdown', 0):.2f}")
    print(f"Net PnL:      {stats.get('Total PnL', 0):.2f}")

if __name__ == "__main__":
    main()
