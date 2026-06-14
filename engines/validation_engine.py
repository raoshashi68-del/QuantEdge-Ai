"""
==========================================================

QuantEdge AI

Validation Engine

Responsibilities
----------------
1. Validate candidate
2. Reject bad liquidity
3. Reject bad spread
4. Reject bad RR
5. Reject missing Greeks

==========================================================
"""


class ValidationEngine:

    def __init__(

        self,

        min_probability=65,

        min_rr=2.0,

        max_spread=1.5,

        min_oi=10000,

        min_volume=1000,

    ):

        self.min_probability = min_probability
        self.min_rr = min_rr
        self.max_spread = max_spread
        self.min_oi = min_oi
        self.min_volume = min_volume

    # ---------------------------------------

    def validate(self, candidate):

        errors = []

        if candidate.probability < self.min_probability:

            errors.append(
                "LOW_PROBABILITY"
            )

        if candidate.risk_reward < self.min_rr:

            errors.append(
                "LOW_RR"
            )

        if candidate.spread > self.max_spread:

            errors.append(
                "HIGH_SPREAD"
            )

        if candidate.open_interest < self.min_oi:

            errors.append(
                "LOW_OI"
            )

        if candidate.volume < self.min_volume:

            errors.append(
                "LOW_VOLUME"
            )

        if candidate.delta == 0:

            errors.append(
                "DELTA_MISSING"
            )

        if candidate.implied_volatility == 0:

            errors.append(
                "IV_MISSING"
            )

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }

    # ---------------------------------------

    def validate_all(

        self,

        candidates,

    ):

        accepted = []

        rejected = []

        for c in candidates:

            result = self.validate(c)

            if result["valid"]:

                accepted.append(c)

            else:

                rejected.append(

                    {

                        "candidate": c,

                        "errors": result["errors"]

                    }

                )

        return accepted, rejected