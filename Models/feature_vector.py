"""
==========================================================

QuantEdge AI

Feature Vector

This object stores EVERY feature computed for a stock.

No engine should pass raw dictionaries.

==========================================================
"""

from dataclasses import dataclass


@dataclass
class FeatureVector:

    # -------------------------

    symbol: str

    close: float

    # -------------------------

    ema9: float = 0.0

    ema20: float = 0.0

    ema50: float = 0.0

    # -------------------------

    rsi: float = 0.0

    macd: float = 0.0

    macd_signal: float = 0.0

    macd_hist: float = 0.0

    # -------------------------

    atr: float = 0.0

    adx: float = 0.0

    supertrend: float = 0.0

    supertrend_direction: float = 0.0

    # -------------------------

    vwap: float = 0.0

    relative_volume: float = 0.0

    orb_high: float = 0.0

    orb_low: float = 0.0

    # -------------------------

    sector_strength: float = 0.0

    relative_strength: float = 0.0

    # -------------------------

    delta: float = 0.0

    gamma: float = 0.0

    theta: float = 0.0

    vega: float = 0.0

    implied_volatility: float = 0.0

    # -------------------------

    spread_percent: float = 0.0

    liquidity_score: float = 0.0

    open_interest: int = 0

    option_volume: int = 0