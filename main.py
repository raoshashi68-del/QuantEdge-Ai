"""
==========================================================

QuantEdge AI

Main Application

==========================================================
"""

import time
from datetime import datetime

from core.controller import Controller
from core.universe_manager import UniverseManager

from engines.data_engine import DataEngine
from engines.feature_engine import FeatureEngine
from engines.option_chain_parser import OptionChainParser
from engines.strike_selector import StrikeSelector
from engines.candidate_engine import CandidateEngine
from engines.filter_engine import FilterEngine
from engines.ranking_engine import RankingEngine
from engines.decision_engine import DecisionEngine
from engines.session_manager import SessionManager
from paper_trading.paper_broker import PaperBroker
from core.live_scan_pipeline import LiveScanPipeline

from core.constants import (
    EXECUTE,
    MARKET_CLOSED,
    FORCE_EXIT,
)


from brokers.fyers_broker import FyersBroker
import os
from dotenv import load_dotenv
from engines.evidence_engine import EvidenceEngine
from engines.evidence_engine import EvidenceEngine
from engines.probability_engine import ProbabilityEngine
from engines.expected_return_engine import ExpectedReturnEngine
from engines.risk_engine import RiskEngine
from engines.expected_value_engine import ExpectedValueEngine
from engines.confidence_engine import ConfidenceEngine

def build_controller(universe):

    # Define paths to the yfinance auth storage
    YFINANCE_DIR = r"C:\Users\c.k.shashi.shekhar\Desktop\yfinance"
    env_path = os.path.join(YFINANCE_DIR, ".env")
    token_path = os.path.join(YFINANCE_DIR, "fyers_token.txt")

    # Load CLIENT_ID
    load_dotenv(env_path)
    client_id = os.getenv("FYERS_APP_ID")

    # Load ACCESS_TOKEN
    access_token = ""
    if os.path.exists(token_path):
        with open(token_path, "r") as f:
            access_token = f.read().strip()

    # Instantiate real market data provider with loaded credentials
    market_data_provider = FyersBroker(
        client_id=client_id,
        access_token=access_token
    )

    # Inject market data provider into the paper execution simulator
    broker = PaperBroker(market_data_provider=market_data_provider)
    data_engine = DataEngine(broker=broker)
    feature_engine = FeatureEngine()
    option_chain_parser = OptionChainParser()
    strike_selector = StrikeSelector()
    candidate_engine = CandidateEngine()
    filter_engine = FilterEngine()
    ranking_engine = RankingEngine()
    decision_engine = DecisionEngine()
    
    # Institutional Stack
    evidence_engine = EvidenceEngine()
    probability_engine = ProbabilityEngine()
    expected_return_engine = ExpectedReturnEngine()
    risk_engine = RiskEngine()
    expected_value_engine = ExpectedValueEngine()
    confidence_engine = ConfidenceEngine()

    pipeline = LiveScanPipeline(
        universe_manager=universe,
        data_engine=data_engine,
        feature_engine=feature_engine,
        option_chain_parser=option_chain_parser,
        strike_selector=strike_selector,
        candidate_engine=candidate_engine,
        filter_engine=filter_engine,
        ranking_engine=ranking_engine,
        decision_engine=decision_engine,
        evidence_engine=evidence_engine,
        probability_engine=probability_engine,
        expected_return_engine=expected_return_engine,
        risk_engine=risk_engine,
        expected_value_engine=expected_value_engine,
        confidence_engine=confidence_engine,
    )

    return Controller(pipeline=pipeline)


def load_universe():

    universe = UniverseManager()

    universe.add_many([
        "HAL",
        "BEL",
        "SBIN",
        "RELIANCE",
        "TCS",
        "INFY",
    ])

    return universe


def print_banner():

    print("=" * 60)
    print("QuantEdge AI")
    print("Institutional Intraday Scanner")
    print("=" * 60)


def main():

    print_banner()

    session = SessionManager()

    universe = load_universe()

    controller = build_controller(universe)

    while True:

        status = session.status()

        if status == MARKET_CLOSED:

            print("Market Closed")

            time.sleep(60)

            continue

        if status == FORCE_EXIT:

            print("Force Exit Window")

            time.sleep(30)

            continue

        print()

        print("----------------------------------------")

        print(datetime.now())

        print("----------------------------------------")

        result = controller.run()

        decision = result["decision"]

        if decision is None or (not hasattr(decision, 'action') and not isinstance(decision, dict)):
            print("No candidates found")

        elif (hasattr(decision, 'action') and decision.action == "EXECUTE") or (isinstance(decision, dict) and decision.get('action') == "EXECUTE"):
            c = decision.candidate if hasattr(decision, 'candidate') else decision.get('candidate')
            
            print()
            print(f"Rank: {c.rank}")
            print(f"Symbol: {c.symbol}")
            print(f"Action: EXECUTE")
            print()
            print(f"Expected Value : {c.expected_value_result.expected_value:.4f}")
            print(f"Confidence      : {c.confidence_result.confidence:.4f}")
            print(f"Probability     : {c.probability_result.probability:.4f}")
            print(f"Expected Return : {c.expected_return_result.expected_return:.4f}")
            print(f"Expected Loss   : {c.risk_result.expected_loss:.4f}")
            print(f"Final Score     : {c.score:.4f}")
            print(f"Decision Reason : {getattr(decision, 'reason', '')}")
            print()

        else:
            action = getattr(decision, 'action', '') if hasattr(decision, 'action') else decision.get('action', 'NO_TRADE')
            reason = getattr(decision, 'reason', '') if hasattr(decision, 'reason') else decision.get('reason', 'UNKNOWN')
            print()
            print(f"Action: {action}")
            print(f"Decision Reason: {reason}")
            print()

        time.sleep(60)


if __name__ == "__main__":

    main()