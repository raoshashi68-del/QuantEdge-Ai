"""
==========================================================

QuantEdge AI

Option Analytics Engine

Responsibilities
----------------
1. Compute expected option move
2. Compute reward/risk
3. Compute liquidity score
4. Compute spread score
5. Compute option quality

==========================================================
"""

from dataclasses import dataclass


@dataclass
class OptionAnalysis:

    expected_move: float

    reward_risk: float

    liquidity_score: float

    spread_score: float

    quality_score: float


class OptionAnalytics:

    @staticmethod
    def expected_option_move(

        delta,

        gamma,

        theta,

        expected_stock_move,

        time_fraction,

    ):

        return (

            delta * expected_stock_move

            +

            0.5 * gamma * (expected_stock_move ** 2)

            +

            theta * time_fraction

        )

    @staticmethod
    def reward_risk(

        entry,

        target,

        stop,

    ):

        reward = target - entry

        risk = entry - stop

        if risk <= 0:

            return 0.0

        return reward / risk

    @staticmethod
    def liquidity_score(

        open_interest,

        volume,

    ):

        score = 0

        if open_interest >= 500000:

            score += 50

        elif open_interest >= 100000:

            score += 35

        elif open_interest >= 25000:

            score += 20

        if volume >= 100000:

            score += 50

        elif volume >= 25000:

            score += 35

        elif volume >= 5000:

            score += 20

        return min(score, 100)

    @staticmethod
    def spread_score(

        spread_percent,

    ):

        if spread_percent <= 0.25:

            return 100

        if spread_percent <= 0.50:

            return 90

        if spread_percent <= 1.00:

            return 75

        if spread_percent <= 2.00:

            return 50

        return 0

    @classmethod
    def analyze(

        cls,

        delta,

        gamma,

        theta,

        expected_stock_move,

        time_fraction,

        entry,

        target,

        stop,

        open_interest,

        volume,

        spread_percent,

    ):

        expected_move = cls.expected_option_move(

            delta,

            gamma,

            theta,

            expected_stock_move,

            time_fraction,

        )

        rr = cls.reward_risk(

            entry,

            target,

            stop,

        )

        liquidity = cls.liquidity_score(

            open_interest,

            volume,

        )

        spread = cls.spread_score(

            spread_percent,

        )

        quality = (

            0.4 * liquidity

            +

            0.3 * spread

            +

            0.3 * min(rr * 25, 100)

        )

        return OptionAnalysis(

            expected_move=expected_move,

            reward_risk=rr,

            liquidity_score=liquidity,

            spread_score=spread,

            quality_score=quality,

        )