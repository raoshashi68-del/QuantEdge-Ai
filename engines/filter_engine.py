"""
==========================================================

QuantEdge AI

Filter Engine

Responsibilities

1. Reject illiquid trades
2. Reject wide spreads
3. Reject low OI
4. Reject low volume
5. Reject weak ADX
6. Return filtered candidates

==========================================================
"""

from config.settings import (
    MIN_ADX,
    MIN_VOLUME,
    MIN_OI,
    MAX_SPREAD_PERCENT,
)


class FilterEngine:

    def __init__(self):
        pass

    def apply(self, candidate):

        # ----------------------------
        # ADX
        # ----------------------------

        adx = candidate.get_feature("adx", 0)

        if adx < MIN_ADX:

            candidate.reject("ADX_TOO_LOW")

            return candidate

        # ----------------------------
        # Relative Volume
        # ----------------------------

        rel_volume = candidate.get_feature(
            "relative_volume",
            0
        )

        if rel_volume < 1:

            candidate.reject("LOW_RELATIVE_VOLUME")

            return candidate

        # ----------------------------
        # Option Volume
        # ----------------------------

        if candidate.volume < MIN_VOLUME:

            candidate.reject("LOW_OPTION_VOLUME")

            return candidate

        # ----------------------------
        # Open Interest
        # ----------------------------

        if candidate.open_interest < MIN_OI:

            candidate.reject("LOW_OPEN_INTEREST")

            return candidate

        # ----------------------------
        # Spread
        # ----------------------------

        if candidate.spread > MAX_SPREAD_PERCENT:

            candidate.reject("SPREAD_TOO_WIDE")

            return candidate

        candidate.state = "FILTERED"

        return candidate

    def apply_all(self, candidates):

        accepted = []

        rejected = []

        for candidate in candidates:

            candidate = self.apply(candidate)

            if candidate.execute is False and \
               candidate.rejection_reason is not None:

                rejected.append(candidate)

            else:

                accepted.append(candidate)

        return accepted, rejected