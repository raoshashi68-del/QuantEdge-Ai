"""
==========================================================

QuantEdge AI

Risk Manager

Responsibilities
----------------
1. Position sizing
2. Capital allocation
3. Risk calculation
4. Lot calculation
5. Trade validation

==========================================================
"""

from dataclasses import dataclass
from math import floor


@dataclass
class RiskResult:

    approved: bool

    quantity: int

    lots: int

    capital_required: float

    max_loss: float

    risk_percent: float

    reason: str


class RiskManager:

    def __init__(

        self,

        capital,

        max_risk_percent=1.0,

        max_capital_percent=100.0,

    ):

        self.capital = capital

        self.max_risk_percent = max_risk_percent

        self.max_capital_percent = max_capital_percent

    # ------------------------------------------------

    def calculate(

        self,

        option_price,

        stop_loss_price,

        lot_size,

    ):

        if option_price <= 0:

            return RiskResult(

                False,

                0,

                0,

                0,

                0,

                0,

                "INVALID_OPTION_PRICE"

            )

        risk_per_unit = option_price - stop_loss_price

        if risk_per_unit <= 0:

            return RiskResult(

                False,

                0,

                0,

                0,

                0,

                0,

                "INVALID_STOP_LOSS"

            )

        max_rupee_risk = (

            self.capital *

            self.max_risk_percent

        ) / 100

        quantity = floor(

            max_rupee_risk /

            risk_per_unit

        )

        lots = quantity // lot_size

        quantity = lots * lot_size

        capital_required = (

            quantity *

            option_price

        )

        if capital_required > (

            self.capital *

            self.max_capital_percent

        ) / 100:

            return RiskResult(

                False,

                0,

                0,

                capital_required,

                max_rupee_risk,

                self.max_risk_percent,

                "INSUFFICIENT_CAPITAL"

            )

        return RiskResult(

            True,

            quantity,

            lots,

            capital_required,

            quantity * risk_per_unit,

            self.max_risk_percent,

            "APPROVED"

        )

    # ------------------------------------------------

    @staticmethod
    def reward_risk(

        target,

        entry,

        stop,

    ):

        reward = target - entry

        risk = entry - stop

        if risk <= 0:

            return 0

        return reward / risk

    # ------------------------------------------------

    @staticmethod
    def expected_value(

        probability,

        reward,

        risk,

    ):

        probability = probability / 100

        return (

            probability * reward

            -

            (1 - probability) * risk

        )