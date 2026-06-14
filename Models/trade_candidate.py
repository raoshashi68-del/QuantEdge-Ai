"""
==========================================================

QuantEdge AI

Trade Candidate

Universal object passed between all engines.

==========================================================
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class TradeCandidate:

    # -----------------------------------------
    # Identity
    # -----------------------------------------

    symbol: str

    direction: str

    option_symbol: str

    strike: float

    expiry: str

    # -----------------------------------------
    # Prices
    # -----------------------------------------

    stock_price: float

    option_price: float

    bid: float = 0.0

    ask: float = 0.0

    spread: float = 0.0

    # -----------------------------------------
    # Liquidity
    # -----------------------------------------

    volume: int = 0

    open_interest: int = 0

    liquidity_score: float = 0.0

    # -----------------------------------------
    # Greeks
    # -----------------------------------------

    implied_volatility: float = 0.0

    delta: float = 0.0

    gamma: float = 0.0

    theta: float = 0.0

    vega: float = 0.0

    # -----------------------------------------
    # Strategy
    # -----------------------------------------

    probability: float = 0.0

    confidence: float = 0.0

    expected_return: float = 0.0

    expected_value: float = 0.0

    risk_reward: float = 0.0

    score: float = 0.0

    rank: int = 0

    # -----------------------------------------
    # State
    # -----------------------------------------

    execute: bool = False

    rejection_reason: Optional[str] = None

    state: str = "NEW"

    # -----------------------------------------
    # Features
    # -----------------------------------------

    features: Dict = field(default_factory=dict)

    # -----------------------------------------

    def add_feature(self, key, value):

        self.features[key] = value

    # -----------------------------------------

    def get_feature(self, key, default=None):

        return self.features.get(key, default)

    # -----------------------------------------

    def reject(self, reason):

        self.execute = False

        self.rejection_reason = reason

        self.state = "REJECTED"

    # -----------------------------------------

    def approve(self):

        self.execute = True

        self.rejection_reason = None

        self.state = "APPROVED"

    # -----------------------------------------

    def to_dict(self):

        return {

            "symbol": self.symbol,

            "direction": self.direction,

            "option_symbol": self.option_symbol,

            "strike": self.strike,

            "expiry": self.expiry,

            "stock_price": self.stock_price,

            "option_price": self.option_price,

            "probability": self.probability,

            "confidence": self.confidence,

            "expected_return": self.expected_return,

            "expected_value": self.expected_value,

            "risk_reward": self.risk_reward,

            "score": self.score,

            "rank": self.rank,

            "state": self.state,

        }