"""
==========================================================

QuantEdge AI

Greeks Engine

Responsibilities
----------------
1. Delta
2. Gamma
3. Theta
4. Vega

==========================================================
"""

import math

from scipy.stats import norm

from engines.black_scholes import BlackScholes


class GreeksEngine:

    @staticmethod
    def delta_call(
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

        return norm.cdf(d1)

    @staticmethod
    def delta_put(
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

        return norm.cdf(d1) - 1

    @staticmethod
    def gamma(
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

        return (

            norm.pdf(d1)

            /

            (

                S

                *

                sigma

                *

                math.sqrt(T)

            )

        )

    @staticmethod
    def vega(
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

        return (

            S

            *

            norm.pdf(d1)

            *

            math.sqrt(T)

        ) / 100

    @staticmethod
    def theta_call(
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

        term1 = (

            -S

            *

            norm.pdf(d1)

            *

            sigma

        ) / (

            2

            *

            math.sqrt(T)

        )

        term2 = (

            -r

            *

            K

            *

            math.exp(

                -r * T

            )

            *

            norm.cdf(d2)

        )

        return (

            term1

            +

            term2

        ) / 365

    @staticmethod
    def theta_put(
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

        term1 = (

            -S

            *

            norm.pdf(d1)

            *

            sigma

        ) / (

            2

            *

            math.sqrt(T)

        )

        term2 = (

            r

            *

            K

            *

            math.exp(

                -r * T

            )

            *

            norm.cdf(-d2)

        )

        return (

            term1

            +

            term2

        ) / 365