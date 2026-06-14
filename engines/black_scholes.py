"""
==========================================================

QuantEdge AI

Black-Scholes Pricing Engine

Responsibilities
----------------
1. Compute Option Price
2. Compute d1
3. Compute d2

==========================================================
"""

import math
from scipy.stats import norm


class BlackScholes:

    @staticmethod
    def d1(
        S,
        K,
        T,
        r,
        sigma,
    ):

        return (

            math.log(S / K)

            +

            (

                r +

                0.5 * sigma ** 2

            ) * T

        ) / (

            sigma *

            math.sqrt(T)

        )

    @staticmethod
    def d2(
        S,
        K,
        T,
        r,
        sigma,
    ):

        return (

            BlackScholes.d1(

                S,

                K,

                T,

                r,

                sigma,

            )

            -

            sigma *

            math.sqrt(T)

        )

    @staticmethod
    def call_price(
        S,
        K,
        T,
        r,
        sigma,
    ):

        d1 = BlackScholes.d1(
            S,
            K,
            T,
            r,
            sigma,
        )

        d2 = BlackScholes.d2(
            S,
            K,
            T,
            r,
            sigma,
        )

        return (

            S *

            norm.cdf(d1)

            -

            K *

            math.exp(

                -r * T

            ) *

            norm.cdf(d2)

        )

    @staticmethod
    def put_price(
        S,
        K,
        T,
        r,
        sigma,
    ):

        d1 = BlackScholes.d1(
            S,
            K,
            T,
            r,
            sigma,
        )

        d2 = BlackScholes.d2(
            S,
            K,
            T,
            r,
            sigma,
        )

        return (

            K *

            math.exp(

                -r * T

            ) *

            norm.cdf(-d2)

            -

            S *

            norm.cdf(-d1)

        )