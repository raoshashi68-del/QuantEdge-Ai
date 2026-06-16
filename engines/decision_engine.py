"""
==========================================================
QuantEdge AI
Decision Engine v2
==========================================================
"""
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Decision:
    action: str
    candidate: Optional[object]
    reason: str

class DecisionEngine:
    def __init__(
        self,
        minimum_confidence=0.50,
        minimum_probability=0.50
    ):
        self.minimum_confidence = minimum_confidence
        self.minimum_probability = minimum_probability

    def decide(self, ranked_candidates: List) -> Decision:
        if not ranked_candidates:
            return Decision(
                action="NO_TRADE",
                candidate=None,
                reason="NO_CANDIDATES"
            )

        best = ranked_candidates[0]
        
        # Safely extract values
        ev = best.expected_value_result.expected_value if best.expected_value_result else 0.0
        conf = best.confidence_result.confidence if best.confidence_result else 0.0
        prob = best.probability_result.probability if best.probability_result else 0.0

        if ev <= 0:
            return Decision(
                action="NO_TRADE",
                candidate=None,
                reason="NEGATIVE_EXPECTED_VALUE"
            )

        if conf < self.minimum_confidence:
            return Decision(
                action="NO_TRADE",
                candidate=None,
                reason="LOW_CONFIDENCE"
            )

        if prob < self.minimum_probability:
            return Decision(
                action="NO_TRADE",
                candidate=None,
                reason="LOW_PROBABILITY"
            )

        best.approve()

        return Decision(
            action="EXECUTE",
            candidate=best,
            reason="BEST_OPPORTUNITY"
        )