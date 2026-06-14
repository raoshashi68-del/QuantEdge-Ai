"""
==========================================================

QuantEdge AI

Market Snapshot Model

==========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class MarketSnapshot:

    # ----------------------------------------
    # Time
    # ----------------------------------------

    timestamp: datetime = field(
        default_factory=datetime.now
    )

    # ----------------------------------------
    # Index Data
    # ----------------------------------------

    nifty: float = 0.0

    banknifty: float = 0.0

    finnifty: float = 0.0

    midcap: float = 0.0

    vix: float = 0.0

    # ----------------------------------------
    # Daily Change
    # ----------------------------------------

    nifty_change: float = 0.0

    banknifty_change: float = 0.0

    finnifty_change: float = 0.0

    midcap_change: float = 0.0

    vix_change: float = 0.0

    # ----------------------------------------
    # Breadth
    # ----------------------------------------

    advancing: int = 0

    declining: int = 0

    unchanged: int = 0

    # ----------------------------------------
    # Sector Strength
    # ----------------------------------------

    sectors: Dict = field(
        default_factory=dict
    )

    # ----------------------------------------
    # Liquidity
    # ----------------------------------------

    market_volume: float = 0.0

    relative_volume: float = 0.0

    # ----------------------------------------
    # Regime
    # ----------------------------------------

    regime: str = "UNKNOWN"

    # ----------------------------------------
    # Methods
    # ----------------------------------------

    @property
    def breadth_ratio(self):

        total = (
            self.advancing +
            self.declining
        )

        if total == 0:

            return 0

        return self.advancing / total

    def set_sector_strength(
        self,
        sector,
        strength
    ):

        self.sectors[sector] = strength

    def get_sector_strength(
        self,
        sector
    ):

        return self.sectors.get(
            sector,
            0
        )

    def summary(self):

        return {

            "time":
            self.timestamp,

            "nifty":
            self.nifty,

            "banknifty":
            self.banknifty,

            "vix":
            self.vix,

            "breadth":
            self.breadth_ratio,

            "regime":
            self.regime

        }