"""
==========================================================

QuantEdge AI

Option Chain Selector

Responsibilities
----------------
1. Fetch option chain
2. Separate CE and PE
3. Score liquidity
4. Select best strike

==========================================================
"""

from typing import List, Dict


class OptionChainSelector:

    def __init__(self):
        pass

    @staticmethod
    def liquidity_score(option: Dict) -> float:

        oi = option.get("open_interest", 0)
        volume = option.get("volume", 0)
        spread = option.get("spread_percent", 100)

        score = 0.0

        score += min(oi / 500000, 1.0) * 40
        score += min(volume / 100000, 1.0) * 40
        score += max(0.0, 1 - spread / 5.0) * 20

        return score

    @staticmethod
    def filter_side(
        chain: List[Dict],
        side: str,
    ):

        return [

            option

            for option in chain

            if option.get("type") == side

        ]

    def best_option(

        self,

        chain: List[Dict],

        side: str,

    ):

        options = self.filter_side(

            chain,

            side,

        )

        if len(options) == 0:

            return None

        best = None
        best_score = -1

        for option in options:

            score = self.liquidity_score(option)

            if score > best_score:

                best_score = score
                best = option

        return best

    def select(

        self,

        chain: List[Dict],

    ):

        ce = self.best_option(

            chain,

            "CE",

        )

        pe = self.best_option(

            chain,

            "PE",

        )

        return {

            "CE": ce,

            "PE": pe,

        }