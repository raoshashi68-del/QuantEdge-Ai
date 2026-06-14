"""
==========================================================

QuantEdge AI

Global Constants

==========================================================
"""

# =====================================================
# STATES
# =====================================================

NEW = "NEW"

PENDING = "PENDING"

APPROVED = "APPROVED"

REJECTED = "REJECTED"

EXECUTED = "EXECUTED"

CLOSED = "CLOSED"

# =====================================================
# DIRECTIONS
# =====================================================

CALL = "CE"

PUT = "PE"

BUY = "BUY"

SELL = "SELL"

# =====================================================
# DECISIONS
# =====================================================

EXECUTE = "EXECUTE"

NO_TRADE = "NO_TRADE"

# =====================================================
# FILTER REASONS
# =====================================================

LOW_PROBABILITY = "LOW_PROBABILITY"

LOW_RR = "LOW_RISK_REWARD"

LOW_VOLUME = "LOW_VOLUME"

LOW_OI = "LOW_OPEN_INTEREST"

HIGH_SPREAD = "HIGH_SPREAD"

LOW_ADX = "LOW_ADX"

IV_MISSING = "IV_MISSING"

DELTA_MISSING = "DELTA_MISSING"

# =====================================================
# MARKET STATUS
# =====================================================

MARKET_CLOSED = "MARKET_CLOSED"

ENTRY_ALLOWED = "ENTRY_ALLOWED"

NO_NEW_ENTRY = "NO_NEW_ENTRY"

FORCE_EXIT = "FORCE_EXIT"

# =====================================================
# ORDER TYPES
# =====================================================

MARKET = "MARKET"

LIMIT = "LIMIT"

# =====================================================
# PRODUCTS
# =====================================================

INTRADAY = "INTRADAY"

DELIVERY = "DELIVERY"