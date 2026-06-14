"""
==========================================================

QuantEdge AI

Scoring Engine

Responsibilities
----------------
1. Calculate Technical Score
2. Calculate Liquidity Score
3. Calculate Option Score
4. Calculate Final Score

==========================================================
"""

class ScoringEngine:

    def __init__(self):

        self.weights = {

            "adx":15,

            "relative_volume":15,

            "relative_strength":10,

            "sector_strength":10,

            "vwap":10,

            "orb":5,

            "liquidity":10,

            "spread":10,

            "oi":5,

            "delta":5,

            "gamma":2,

            "theta":1,

            "iv":2

        }

    # -----------------------------------------

    @staticmethod
    def clamp(value):

        return max(0, min(100, value))

    # -----------------------------------------

    def score(self, candidate):

        score = 0

        f = candidate.features

        score += min(
            f.get("adx",0)/40,
            1
        ) * self.weights["adx"]

        score += min(
            f.get("relative_volume",0)/4,
            1
        ) * self.weights["relative_volume"]

        score += min(
            f.get("relative_strength",0)/3,
            1
        ) * self.weights["relative_strength"]

        score += min(
            f.get("sector_strength",0)/3,
            1
        ) * self.weights["sector_strength"]

        score += min(
            f.get("vwap_score",0),
            1
        ) * self.weights["vwap"]

        score += min(
            f.get("orb_score",0),
            1
        ) * self.weights["orb"]

        score += min(
            candidate.liquidity_score/100,
            1
        ) * self.weights["liquidity"]

        spread_score = max(

            0,

            1 -

            candidate.spread/2

        )

        score += spread_score * self.weights["spread"]

        score += min(

            candidate.open_interest/

            500000,

            1

        ) * self.weights["oi"]

        score += min(

            abs(candidate.delta),

            1

        ) * self.weights["delta"]

        score += min(

            candidate.gamma*100,

            1

        ) * self.weights["gamma"]

        score += min(

            abs(candidate.theta)/5,

            1

        ) * self.weights["theta"]

        score += min(

            candidate.implied_volatility/

            50,

            1

        ) * self.weights["iv"]

        return round(

            self.clamp(score),

            2

        )