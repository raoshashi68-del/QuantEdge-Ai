"""
==========================================================

QuantEdge AI

Trade Journal Model

==========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class TradeJournal:

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    trade_id: str

    symbol: str

    direction: str

    option_symbol: str

    # --------------------------------------------------
    # Entry
    # --------------------------------------------------

    entry_time: datetime

    entry_price: float

    quantity: int

    # --------------------------------------------------
    # Exit
    # --------------------------------------------------

    exit_time: Optional[datetime] = None

    exit_price: Optional[float] = None

    exit_reason: str = ""

    # --------------------------------------------------
    # Performance
    # --------------------------------------------------

    pnl: float = 0.0

    pnl_percent: float = 0.0

    holding_minutes: float = 0.0

    # --------------------------------------------------
    # Decision Metrics
    # --------------------------------------------------

    technical_score: float = 0.0

    probability: float = 0.0

    expected_value: float = 0.0

    confidence: float = 0.0

    risk_reward: float = 0.0

    # --------------------------------------------------
    # Feature Snapshot
    # --------------------------------------------------

    features: Dict = field(default_factory=dict)

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    tags: Dict = field(default_factory=dict)

    notes: str = ""

    # --------------------------------------------------
    # Methods
    # --------------------------------------------------

    def add_feature(self, key, value):

        self.features[key] = value

    def add_tag(self, key, value):

        self.tags[key] = value

    def close_trade(
        self,
        exit_price,
        exit_time,
        reason
    ):

        self.exit_price = exit_price

        self.exit_time = exit_time

        self.exit_reason = reason

        self.pnl = (
            exit_price -
            self.entry_price
        ) * self.quantity

        if self.entry_price != 0:

            self.pnl_percent = (
                (
                    exit_price -
                    self.entry_price
                )
                /
                self.entry_price
            ) * 100

        self.holding_minutes = (

            exit_time -
            self.entry_time

        ).total_seconds() / 60

    def summary(self):

        return {

            "trade_id":
            self.trade_id,

            "symbol":
            self.symbol,

            "direction":
            self.direction,

            "pnl":
            self.pnl,

            "pnl_percent":
            self.pnl_percent,

            "holding_minutes":
            self.holding_minutes,

            "confidence":
            self.confidence

        }