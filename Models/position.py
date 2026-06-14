"""
==========================================================

QuantEdge AI

Position Model

==========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Position:

    # ------------------------------------------------
    # Identity
    # ------------------------------------------------

    symbol: str

    direction: str

    option_symbol: str

    # ------------------------------------------------
    # Entry
    # ------------------------------------------------

    quantity: int

    entry_price: float

    entry_time: datetime = field(default_factory=datetime.now)

    # ------------------------------------------------
    # Live
    # ------------------------------------------------

    current_price: float = 0.0

    highest_price: float = 0.0

    lowest_price: float = 0.0

    # ------------------------------------------------
    # Risk
    # ------------------------------------------------

    stop_loss: float = 0.0

    target: float = 0.0

    trailing_stop: float = 0.0

    # ------------------------------------------------
    # Status
    # ------------------------------------------------

    status: str = "OPEN"

    exit_reason: Optional[str] = None

    exit_price: Optional[float] = None

    exit_time: Optional[datetime] = None

    # ------------------------------------------------
    # Statistics
    # ------------------------------------------------

    unrealized_pnl: float = 0.0

    realized_pnl: float = 0.0

    max_profit: float = 0.0

    max_loss: float = 0.0

    # ------------------------------------------------
    # Methods
    # ------------------------------------------------

    def update_price(self, price: float):

        self.current_price = price

        if self.highest_price == 0:
            self.highest_price = price

        self.highest_price = max(
            self.highest_price,
            price
        )

        if self.lowest_price == 0:
            self.lowest_price = price

        self.lowest_price = min(
            self.lowest_price,
            price
        )

        self.unrealized_pnl = (
            price - self.entry_price
        ) * self.quantity

        self.max_profit = max(
            self.max_profit,
            self.unrealized_pnl
        )

        self.max_loss = min(
            self.max_loss,
            self.unrealized_pnl
        )

    def move_trailing_stop(self, new_stop: float):

        if new_stop > self.trailing_stop:

            self.trailing_stop = new_stop

    def close(
        self,
        exit_price: float,
        reason: str
    ):

        self.exit_price = exit_price

        self.exit_reason = reason

        self.exit_time = datetime.now()

        self.status = "CLOSED"

        self.realized_pnl = (
            exit_price - self.entry_price
        ) * self.quantity

    @property
    def pnl_percent(self):

        if self.entry_price == 0:

            return 0

        return (
            (self.current_price - self.entry_price)
            /
            self.entry_price
        ) * 100

    def summary(self):

        return {

            "symbol": self.symbol,

            "direction": self.direction,

            "status": self.status,

            "entry": self.entry_price,

            "current": self.current_price,

            "pnl": self.unrealized_pnl,

            "pnl_percent": self.pnl_percent,

            "target": self.target,

            "stop_loss": self.stop_loss,

            "trailing_stop": self.trailing_stop

        }