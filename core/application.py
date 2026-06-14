"""
==========================================================

QuantEdge AI

Application Controller

==========================================================
"""

from engines.master_scanner import MasterScanner


class QuantEdgeApplication:

    def __init__(
        self,
        data_engine,
        feature_engine,
        candidate_engine,
        filter_engine,
        ranking_engine,
        decision_engine,
    ):

        self.scanner = MasterScanner(
            data_engine=data_engine,
            feature_engine=feature_engine,
            candidate_engine=candidate_engine,
            filter_engine=filter_engine,
            ranking_engine=ranking_engine,
            decision_engine=decision_engine,
        )

    def run(self, universe):

        result = self.scanner.scan(universe)

        self.display(result)

        return result

    @staticmethod
    def display(result):

        print()

        print("=" * 70)

        print("QuantEdge AI")

        print("=" * 70)

        print(
            f"Universe Scanned : {result['total_scanned']}"
        )

        print(
            f"Candidates : {result['total_candidates']}"
        )

        print(
            f"Accepted : {len(result['accepted'])}"
        )

        print(
            f"Rejected : {len(result['rejected'])}"
        )

        print()

        decision = result["decision"]

        if decision.action == "NO_TRADE":

            print("ACTION : NO TRADE")

            print(f"Reason : {decision.reason}")

            print("=" * 70)

            return

        candidate = decision.candidate

        print("ACTION : EXECUTE")

        print()

        print(f"Stock : {candidate.symbol}")

        print(f"Direction : {candidate.direction}")

        print(f"Option : {candidate.option_symbol}")

        print(f"Expected Return : {candidate.expected_return}")

        print(f"Confidence : {candidate.confidence}")

        print(f"Risk Reward : {candidate.risk_reward}")

        print("=" * 70)