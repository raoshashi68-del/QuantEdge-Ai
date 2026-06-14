"""
==========================================================

QuantEdge AI

Ranking Engine

Responsibilities
----------------
1. Rank all candidates
2. Compute Expected Value
3. Compute Opportunity Score
4. Return sorted list

==========================================================
"""

from typing import List


class RankingEngine:

    def __init__(self):
        pass

    # ------------------------------------------------
    # Expected Value
    # ------------------------------------------------

    @staticmethod
    def expected_value(probability,
                       reward,
                       risk):

        return (
            probability * reward
            -
            (1 - probability) * risk
        )

    # ------------------------------------------------
    # Technical Score
    # ------------------------------------------------

    @staticmethod
    def technical_score(candidate):

        score = 0

        adx = candidate.get_feature("adx", 0)
        rsi = candidate.get_feature("rsi", 50)
        rel_vol = candidate.get_feature(
            "relative_volume",
            1
        )

        if adx >= 25:
            score += 25
        elif adx >= 20:
            score += 15

        if 55 <= rsi <= 70:
            score += 20

        if rel_vol >= 3:
            score += 20
        elif rel_vol >= 2:
            score += 15
        elif rel_vol >= 1:
            score += 10

        if candidate.spread <= 0.5:
            score += 15

        if candidate.open_interest >= 100000:
            score += 20

        return score

    # ------------------------------------------------
    # Rank
    # ------------------------------------------------

    def rank(
        self,
        candidates: List
    ):

        for candidate in candidates:

            candidate.technical_score = (
                self.technical_score(
                    candidate
                )
            )

            candidate.expected_value = (
                self.expected_value(
                    candidate.probability / 100,
                    candidate.expected_return,
                    max(
                        1,
                        candidate.expected_return /
                        max(candidate.risk_reward, 1)
                    )
                )
            )

        candidates.sort(

            key=lambda x: (

                x.expected_value,

                x.technical_score,

                x.confidence

            ),

            reverse=True

        )

        for rank, candidate in enumerate(
            candidates,
            start=1
        ):

            candidate.rank = rank

            candidate.state = "RANKED"

        return candidates

    # ------------------------------------------------
    # Top N
    # ------------------------------------------------

    @staticmethod
    def top(
        candidates,
        n=10
    ):

        return candidates[:n]

    # ------------------------------------------------
    # Opportunity Gap
    # ------------------------------------------------

    @staticmethod
    def opportunity_gap(
        candidates
    ):

        if len(candidates) < 2:

            return None

        first = candidates[0]

        second = candidates[1]

        return (

            first.expected_value
            -
            second.expected_value

        )