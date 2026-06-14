"""
==========================================================

QuantEdge AI

Strike Selector

Responsibilities
----------------
1. Score every strike
2. Reject illiquid strikes
3. Return best CE
4. Return best PE

==========================================================
"""

from typing import List


class StrikeSelector:

    def __init__(self):

        pass

    @staticmethod
    def score(option):

        score = 0.0

        oi = option.get(
            "open_interest",
            0,
        )

        volume = option.get(
            "volume",
            0,
        )

        spread = option.get(
            "spread_percent",
            100,
        )

        iv = option.get(
            "iv",
            0,
        )

        score += min(
            oi / 500000,
            1,
        ) * 35

        score += min(
            volume / 100000,
            1,
        ) * 35

        score += max(
            0,
            1 - spread / 5,
        ) * 20

        score += min(
            iv / 50,
            1,
        ) * 10

        return score

    def best(

        self,

        options: List,

    ):

        if not options:

            return None

        best_option = None

        best_score = -1

        for option in options:

            s = self.score(option)

            if s > best_score:

                best_score = s

                best_option = option

        return best_option

    def select(

        self,

        ce_options,

        pe_options,

    ):

        return {

            "CE": self.best(

                ce_options,

            ),

            "PE": self.best(

                pe_options,

            ),

        }