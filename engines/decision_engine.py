"""
==========================================================

QuantEdge AI

Decision Engine

Responsibilities
----------------
1. Decide whether to trade
2. Compare Rank 1 vs Rank 2
3. Check minimum quality
4. Return EXECUTE or NO_TRADE

==========================================================
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Decision:

    action: str

    candidate: Optional[object]

    reason: str

    opportunity_gap: float


class DecisionEngine:

    def __init__(

        self,

        minimum_confidence=70,

        minimum_rr=2.0,

        minimum_expected_return=10.0,

        minimum_gap=2.0,

    ):

        self.minimum_confidence = minimum_confidence
        self.minimum_rr = minimum_rr
        self.minimum_expected_return = minimum_expected_return
        self.minimum_gap = minimum_gap

    # --------------------------------------------------

    @staticmethod
    def _gap(first, second):

        gap = first.expected_value - second.expected_value

        return max(0.0, gap)

    # --------------------------------------------------

    def decide(
        self,
        ranked_candidates: List,
    ):

        if len(ranked_candidates) == 0:

            return Decision(

                action="NO_TRADE",

                candidate=None,

                reason="NO_CANDIDATES",

                opportunity_gap=0.0,

            )

        best = ranked_candidates[0]

        if best.confidence < self.minimum_confidence:

            return Decision(

                action="NO_TRADE",

                candidate=None,

                reason="LOW_CONFIDENCE",

                opportunity_gap=0.0,

            )

        if best.risk_reward < self.minimum_rr:

            return Decision(

                action="NO_TRADE",

                candidate=None,

                reason="LOW_RISK_REWARD",

                opportunity_gap=0.0,

            )

        if best.expected_return < self.minimum_expected_return:

            return Decision(

                action="NO_TRADE",

                candidate=None,

                reason="LOW_EXPECTED_RETURN",

                opportunity_gap=0.0,

            )

        if len(ranked_candidates) == 1:

            best.approve()

            return Decision(

                action="EXECUTE",

                candidate=best,

                reason="ONLY_VALID_CANDIDATE",

                opportunity_gap=float("inf"),

            )

        second = ranked_candidates[1]

        gap = self._gap(

            best,

            second,

        )

        if gap < self.minimum_gap:

            return Decision(

                action="NO_TRADE",

                candidate=None,

                reason="OPPORTUNITY_GAP_TOO_SMALL",

                opportunity_gap=gap,

            )

        best.approve()

        return Decision(

            action="EXECUTE",

            candidate=best,

            reason="BEST_OPPORTUNITY",

            opportunity_gap=gap,

        )

    # --------------------------------------------------

    @staticmethod
    def summary(decision):

        if decision.action == "NO_TRADE":

            return {

                "action": decision.action,

                "reason": decision.reason,

                "opportunity_gap": decision.opportunity_gap,

            }

        c = decision.candidate

        return {

            "action": decision.action,

            "symbol": c.symbol,

            "direction": c.direction,

            "confidence": c.confidence,

            "expected_return": c.expected_return,

            "risk_reward": c.risk_reward,

            "expected_value": c.expected_value,

            "score": c.score,

            "gap": decision.opportunity_gap,

            "reason": decision.reason,

        }