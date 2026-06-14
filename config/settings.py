"""
==========================================================

QuantEdge AI

Global Configuration

==========================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:

    # =====================================================
    # APPLICATION
    # =====================================================

    APP_NAME = "QuantEdge AI"
    VERSION = "1.0.0"

    DEBUG = True

    # =====================================================
    # SCANNER
    # =====================================================

    MAX_WORKERS = 16

    SCAN_INTERVAL_SECONDS = 60

    TOP_RESULTS = 10

    # =====================================================
    # MARKET SESSION
    # =====================================================

    MARKET_OPEN = "09:15"

    LAST_ENTRY = "15:00"

    FORCE_EXIT = "15:15"

    MARKET_CLOSE = "15:30"

    # =====================================================
    # DATA
    # =====================================================

    DEFAULT_RESOLUTION = "1"

    HISTORY_DAYS = 30

    HISTORY_CACHE_SECONDS = 30

    QUOTE_CACHE_SECONDS = 2

    OPTION_CHAIN_CACHE_SECONDS = 5

    # =====================================================
    # TREND FILTERS
    # =====================================================

    MIN_ADX = 20

    MIN_RELATIVE_VOLUME = 1.5

    MIN_RSI = 55

    MAX_RSI = 75

    REQUIRE_VWAP = True

    REQUIRE_ORB = True

    # =====================================================
    # LIQUIDITY
    # =====================================================

    MIN_OPEN_INTEREST = 50000

    MIN_OPTION_VOLUME = 10000

    MAX_SPREAD_PERCENT = 1.0

    # =====================================================
    # DECISION
    # =====================================================

    MIN_PROBABILITY = 65.0

    MIN_CONFIDENCE = 70.0

    MIN_EXPECTED_RETURN = 10.0

    MIN_RISK_REWARD = 2.0

    MIN_OPPORTUNITY_GAP = 2.0

    # =====================================================
    # CAPITAL
    # =====================================================

    ACCOUNT_CAPITAL = 100000

    MAX_CAPITAL_PER_TRADE = 100000

    MAX_RISK_PERCENT = 1.0

    # =====================================================
    # OPTIONS
    # =====================================================

    RISK_FREE_RATE = 0.06

    MIN_IV = 0.05

    MAX_IV = 2.00

    DAYS_IN_YEAR = 365

    # =====================================================
    # RANKING WEIGHTS
    # =====================================================

    WEIGHT_SCORE = 0.30

    WEIGHT_EXPECTED_VALUE = 0.30

    WEIGHT_PROBABILITY = 0.20

    WEIGHT_RISK_REWARD = 0.20

    # =====================================================
    # STRIKE SELECTION
    # =====================================================

    TARGET_DELTA_MIN = 0.35

    TARGET_DELTA_MAX = 0.65

    MIN_LIQUIDITY_SCORE = 60

    # =====================================================
    # PAPER TRADING
    # =====================================================

    ENABLE_PAPER_TRADING = True

    SLIPPAGE_PERCENT = 0.10

    BROKERAGE_PER_ORDER = 20

    # =====================================================
    # LOGGING
    # =====================================================

    LOG_FOLDER = "logs"

    SAVE_TRADES = True

    SAVE_REJECTED = True