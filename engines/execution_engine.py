"""
==========================================================

QuantEdge AI

Execution Engine

Responsibilities
----------------
1. Validate decision
2. Build order request
3. Send order to broker
4. Handle failures
5. Return execution result

==========================================================
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ExecutionResult:

    success: bool

    order_id: Optional[str]

    symbol: str

    direction: str

    quantity: int

    message: str

    timestamp: datetime


class ExecutionEngine:

    def __init__(self, broker):

        self.broker = broker

    # -----------------------------------------

    @staticmethod
    def build_order(

        candidate,

        quantity

    ):

        return {

            "symbol": candidate.option_symbol,

            "side": "BUY",

            "quantity": quantity,

            "order_type": "MARKET"

        }

    # -----------------------------------------

    def execute(

        self,

        decision,

        quantity

    ):

        if decision.action != "EXECUTE":

            return ExecutionResult(

                success=False,

                order_id=None,

                symbol="",

                direction="",

                quantity=0,

                message="Decision is NO_TRADE",

                timestamp=datetime.now()

            )

        candidate = decision.candidate

        order = self.build_order(

            candidate,

            quantity

        )

        try:

            response = self.broker.place_order(

                **order

            )

            order_id = response.get(

                "order_id",

                None

            )

            candidate.state = "EXECUTED"

            return ExecutionResult(

                success=True,

                order_id=order_id,

                symbol=candidate.symbol,

                direction=candidate.direction,

                quantity=quantity,

                message="Order Executed",

                timestamp=datetime.now()

            )

        except Exception as e:

            return ExecutionResult(

                success=False,

                order_id=None,

                symbol=candidate.symbol,

                direction=candidate.direction,

                quantity=quantity,

                message=str(e),

                timestamp=datetime.now()

            )

    # -----------------------------------------

    @staticmethod
    def summary(result):

        return {

            "success": result.success,

            "order_id": result.order_id,

            "symbol": result.symbol,

            "direction": result.direction,

            "quantity": result.quantity,

            "message": result.message,

            "timestamp": result.timestamp

        }