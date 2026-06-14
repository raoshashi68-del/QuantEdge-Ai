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

from engines.master_scanner import MasterScanner
from engines.filter_engine import FilterEngine
from engines.ranking_engine import RankingEngine
from engines.decision_engine import DecisionEngine
from engines.session_manager import SessionManager

from core.constants import (
    EXECUTE,
    MARKET_CLOSED,
    FORCE_EXIT,
)


def build_controller():

    scanner = MasterScanner()

    filter_engine = FilterEngine()

    ranking_engine = RankingEngine()

    decision_engine = DecisionEngine()

    return Controller(
        scanner=scanner,
        filter_engine=filter_engine,
        ranking_engine=ranking_engine,
        decision_engine=decision_engine,
    )


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

    controller = build_controller()

    universe = load_universe()

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

        if decision is None:

            print("No candidates found")

        elif decision.action == EXECUTE:

            candidate = decision.candidate

            print()

            print(">>>> EXECUTE <<<<")

            print()

            print("Symbol :", candidate.symbol)

            print("Direction :", candidate.direction)

            print("Option :", candidate.option_symbol)

            print("Score :", candidate.score)

            print("Probability :", candidate.probability)

            print("RR :", candidate.risk_reward)

        else:

            print()

            print(">>>> NO TRADE <<<<")

            print()

            print(decision.reason)

        time.sleep(60)


if __name__ == "__main__":

    main()