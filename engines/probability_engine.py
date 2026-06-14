"""
==========================================================

QuantEdge AI

Probability Engine

Responsibilities
----------------
1. Normalize features
2. Calculate confidence score
3. Estimate probability
4. Return probability object

==========================================================
"""

from dataclasses import dataclass


@dataclass
class ProbabilityResult:

    confidence: float

    probability: float

    passed: bool


class ProbabilityEngine:

    def __init__(

        self,

        minimum_probability=65,

    ):

        self.minimum_probability = minimum_probability

    # ---------------------------------------------

    @staticmethod
    def normalize(

        value,

        minimum,

        maximum,

    ):

        if maximum <= minimum:

            return 0

        value = max(minimum, min(value, maximum))

        return (

            value - minimum

        ) / (

            maximum - minimum

        )

    # ---------------------------------------------

    def calculate(

        self,

        candidate,

    ):

        adx = self.normalize(

            candidate.get_feature(

                "adx",

                0,

            ),

            10,

            50,

        )

        rel_volume = self.normalize(

            candidate.get_feature(

                "relative_volume",

                1,

            ),

            1,

            5,

        )

        rsi = self.normalize(

            candidate.get_feature(

                "rsi",

                50,

            ),

            40,

            80,

        )

        liquidity = min(

            candidate.liquidity_score / 100,

            1,

        )

        score = (

            0.30 * adx

            +

            0.25 * rel_volume

            +

            0.20 * rsi

            +

            0.25 * liquidity

        )

        probability = score * 100

        confidence = probability

        return ProbabilityResult(

            confidence=confidence,

            probability=probability,

            passed=(

                probability >=

                self.minimum_probability

            ),

        )