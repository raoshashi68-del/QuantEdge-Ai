"""
==========================================================
QuantEdge AI
Ranking Engine v2
==========================================================
"""
from typing import List

class RankingEngine:
    def __init__(self):
        pass

    def rank(self, candidates: List):
        for candidate in candidates:
            # Safely extract values (they should exist by this stage)
            ev = candidate.expected_value_result.expected_value if candidate.expected_value_result else 0.0
            conf = candidate.confidence_result.confidence if candidate.confidence_result else 0.0
            prob = candidate.probability_result.probability if candidate.probability_result else 0.0
            
            # Extract evidence metrics and normalize to 0-1
            exec_score = (candidate.evidence.execution / 100.0) if candidate.evidence else 0.0
            cons_score = (candidate.evidence.consistency / 100.0) if candidate.evidence else 0.0
            
            # Mathematical merger for ranking
            final_score = (
                0.50 * ev +
                0.20 * conf +
                0.15 * prob +
                0.10 * exec_score +
                0.05 * cons_score
            )
            
            candidate.score = final_score

        # Sort descending by final score
        candidates.sort(key=lambda x: x.score, reverse=True)

        # Assign rank and state
        for rank, candidate in enumerate(candidates, start=1):
            candidate.rank = rank
            candidate.state = "RANKED"

        return candidates
        
    @staticmethod
    def top(candidates, n=10):
        return candidates[:n]

    @staticmethod
    def opportunity_gap(candidates):
        if len(candidates) < 2:
            return None
        return candidates[0].score - candidates[1].score