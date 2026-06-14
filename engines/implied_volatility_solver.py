# Implied volatility solver
"""
==========================================================

QuantEdge AI

Implied Volatility Solver

Responsibilities
----------------
1. Solve IV from market option price
2. Supports CE and PE
3. Uses Newton-Raphson
4. Returns annualized IV

==========================================================
"""

import math

from engines.black_scholes import BlackScholes
from engines.greeks_engine import GreeksEngine


class ImpliedVolatilitySolver:

    MAX_ITERATIONS = 100

    TOLERANCE = 1e-6

    INITIAL_VOLATILITY = 0.30

    @classmethod
    def solve(

        cls,

        market_price,

        S,

        K,

        T,

        r,

        option_type="CE",

    ):

        sigma = cls.INITIAL_VOLATILITY

        for _ in range(cls.MAX_ITERATIONS):

            if option_type == "CE":

                theoretical = BlackScholes.call_price(

                    S,

                    K,

                    T,

                    r,

                    sigma,

                )

            else:

                theoretical = BlackScholes.put_price(

                    S,

                    K,

                    T,

                    r,

                    sigma,

                )

            diff = theoretical - market_price

            if abs(diff) < cls.TOLERANCE:

                return sigma

            vega = GreeksEngine.vega(

                S,

                K,

                T,

                r,

                sigma,

            )

            if abs(vega) < 1e-10:

                break

            sigma = sigma - diff / vega

            sigma = max(

                0.0001,

                sigma,

            )

        return sigma