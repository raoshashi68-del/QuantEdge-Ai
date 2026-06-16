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


# -------------------------------------------------
# Compatibility aliases
# -------------------------------------------------

MAX_WORKERS = Settings.MAX_WORKERS
SCAN_INTERVAL_SECONDS = Settings.SCAN_INTERVAL_SECONDS
TOP_RESULTS = Settings.TOP_RESULTS

MARKET_OPEN = Settings.MARKET_OPEN
LAST_ENTRY = Settings.LAST_ENTRY
FORCE_EXIT = Settings.FORCE_EXIT
MARKET_CLOSE = Settings.MARKET_CLOSE

DEFAULT_RESOLUTION = Settings.DEFAULT_RESOLUTION
HISTORY_DAYS = Settings.HISTORY_DAYS
HISTORY_CACHE_SECONDS = Settings.HISTORY_CACHE_SECONDS
QUOTE_CACHE_SECONDS = Settings.QUOTE_CACHE_SECONDS
OPTION_CHAIN_CACHE_SECONDS = Settings.OPTION_CHAIN_CACHE_SECONDS

MIN_ADX = Settings.MIN_ADX
MIN_RELATIVE_VOLUME = Settings.MIN_RELATIVE_VOLUME
MIN_RSI = Settings.MIN_RSI
MAX_RSI = Settings.MAX_RSI
REQUIRE_VWAP = Settings.REQUIRE_VWAP
REQUIRE_ORB = Settings.REQUIRE_ORB

MIN_OPEN_INTEREST = Settings.MIN_OPEN_INTEREST
MIN_OPTION_VOLUME = Settings.MIN_OPTION_VOLUME
MAX_SPREAD_PERCENT = Settings.MAX_SPREAD_PERCENT

MIN_PROBABILITY = Settings.MIN_PROBABILITY
MIN_CONFIDENCE = Settings.MIN_CONFIDENCE
MIN_EXPECTED_RETURN = Settings.MIN_EXPECTED_RETURN
MIN_RISK_REWARD = Settings.MIN_RISK_REWARD
MIN_OPPORTUNITY_GAP = Settings.MIN_OPPORTUNITY_GAP

ACCOUNT_CAPITAL = Settings.ACCOUNT_CAPITAL
MAX_CAPITAL_PER_TRADE = Settings.MAX_CAPITAL_PER_TRADE
MAX_RISK_PERCENT = Settings.MAX_RISK_PERCENT

RISK_FREE_RATE = Settings.RISK_FREE_RATE
MIN_IV = Settings.MIN_IV
MAX_IV = Settings.MAX_IV
DAYS_IN_YEAR = Settings.DAYS_IN_YEAR

WEIGHT_SCORE = Settings.WEIGHT_SCORE
WEIGHT_EXPECTED_VALUE = Settings.WEIGHT_EXPECTED_VALUE
WEIGHT_PROBABILITY = Settings.WEIGHT_PROBABILITY
WEIGHT_RISK_REWARD = Settings.WEIGHT_RISK_REWARD

TARGET_DELTA_MIN = Settings.TARGET_DELTA_MIN
TARGET_DELTA_MAX = Settings.TARGET_DELTA_MAX
MIN_LIQUIDITY_SCORE = Settings.MIN_LIQUIDITY_SCORE

ENABLE_PAPER_TRADING = Settings.ENABLE_PAPER_TRADING
SLIPPAGE_PERCENT = Settings.SLIPPAGE_PERCENT
BROKERAGE_PER_ORDER = Settings.BROKERAGE_PER_ORDER

LOG_FOLDER = Settings.LOG_FOLDER
SAVE_TRADES = Settings.SAVE_TRADES
SAVE_REJECTED = Settings.SAVE_REJECTED

APP_NAME = Settings.APP_NAME
VERSION = Settings.VERSION
DEBUG = Settings.DEBUG
