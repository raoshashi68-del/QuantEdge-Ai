"""
==========================================================

QuantEdge AI

Controller

Responsibilities
----------------
1. Run one complete scan cycle
2. Build candidates
3. Filter candidates
4. Rank candidates
5. Make decision

==========================================================
"""


class Controller:

    def __init__(

        self,

        scanner,

        filter_engine,

        ranking_engine,

        decision_engine,

    ):

        self.scanner = scanner

        self.filter_engine = filter_engine

        self.ranking_engine = ranking_engine

        self.decision_engine = decision_engine

    # --------------------------------------------------

    def run(self):

        candidates = self.scanner.scan()

        if not candidates:

            return {

                "decision": None,

                "accepted": [],

                "rejected": []

            }

        accepted, rejected = self.filter_engine.apply_all(

            candidates

        )

        if not accepted:

            return {

                "decision": None,

                "accepted": accepted,

                "rejected": rejected,

            }

        ranked = self.ranking_engine.rank(

            accepted

        )

        decision = self.decision_engine.decide(

            ranked

        )

        return {

            "decision": decision,

            "accepted": accepted,

            "rejected": rejected,

            "ranked": ranked,

        }