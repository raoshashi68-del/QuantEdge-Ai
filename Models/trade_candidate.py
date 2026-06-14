"""
=========================================================

QuantEdge AI

Trade Candidate Model

=========================================================
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime


@dataclass
class TradeCandidate:

    # ------------------------
    # Identity
    # ------------------------

    symbol: str

    direction: str

    option_symbol: str = ""

    sector: str = ""

    # ------------------------
    # Prices
    # ------------------------

    stock_price: float = 0.0

    option_price: float = 0.0

    strike: float = 0.0

    expiry: str = ""

    # ------------------------
    # Feature Store
    # ------------------------

    features: Dict = field(default_factory=dict)

    # ------------------------
    # Metrics
    # ------------------------

    technical_score: float = 0.0

    option_score: float = 0.0

    liquidity_score: float = 0.0

    execution_score: float = 0.0

    expected_value: float = 0.0

    probability: float = 0.0

    expected_return: float = 0.0

    risk_reward: float = 0.0

    confidence: float = 0.0

    # ------------------------
    # Liquidity
    # ------------------------

    spread: float = 0.0

    volume: int = 0

    open_interest: int = 0

    # ------------------------
    # Greeks
    # ------------------------

    implied_volatility: float = 0.0

    delta: float = 0.0

    gamma: float = 0.0

    theta: float = 0.0

    vega: float = 0.0

    # ------------------------
    # Trade Levels
    # ------------------------

    entry_price: float = 0.0

    stop_loss: float = 0.0

    target: float = 0.0

    trailing_stop: float = 0.0

    # ------------------------
    # Decision
    # ------------------------

    state: str = "CREATED"

    execute: bool = False

    rejection_reason: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)

    # ------------------------
    # Methods
    # ------------------------

    def add_feature(self, name: str, value):

        self.features[name] = value

    def get_feature(self, name: str, default=None):

        return self.features.get(name, default)

    def reject(self, reason: str):

        self.execute = False

        self.state = "REJECTED"

        self.rejection_reason = reason

    def approve(self):

        self.execute = True

        self.state = "READY"

    def archive(self):

        self.state = "ARCHIVED"

    def summary(self):

        return {

            "symbol": self.symbol,

            "direction": self.direction,

            "score": self.technical_score,

            "probability": self.probability,

            "expected_return": self.expected_return,

            "risk_reward": self.risk_reward,

            "confidence": self.confidence,

            "state": self.state,

        }