"""
==========================================================

QuantEdge AI

Execution Validation Layer (formerly FilterEngine)

Responsibilities

1. Reject physically impossible or nonsensical options
2. Reject negative/zero prices
3. Reject missing bid/ask
4. Reject negative volume/OI
5. Reject missing/invalid symbols and expiries
6. Return filtered (validated) candidates

==========================================================
"""
import math

class FilterEngine:

    def __init__(self):
        pass

    def apply(self, candidate):

        # ----------------------------
        # Invalid Option Symbol
        # ----------------------------
        if not candidate.option_symbol or not isinstance(candidate.option_symbol, str):
            candidate.reject("INVALID_OPTION_SYMBOL")
            return candidate

        # ----------------------------
        # Missing Expiry
        # ----------------------------
        if not candidate.expiry or not isinstance(candidate.expiry, str):
            candidate.reject("MISSING_EXPIRY")
            return candidate

        # ----------------------------
        # Invalid Prices
        # ----------------------------
        if candidate.option_price <= 0 or math.isnan(candidate.option_price):
            candidate.reject("INVALID_OPTION_PRICE")
            return candidate

        if candidate.stock_price <= 0 or math.isnan(candidate.stock_price):
            candidate.reject("INVALID_STOCK_PRICE")
            return candidate

        # ----------------------------
        # Missing/Invalid Bid/Ask
        # ----------------------------
        if candidate.bid <= 0 or math.isnan(candidate.bid):
            candidate.reject("MISSING_BID")
            return candidate

        if candidate.ask <= 0 or math.isnan(candidate.ask):
            candidate.reject("MISSING_ASK")
            return candidate

        # ----------------------------
        # Invalid Spread
        # ----------------------------
        if candidate.ask < candidate.bid:
            candidate.reject("NEGATIVE_SPREAD")
            return candidate
            
        if math.isnan(candidate.spread):
            candidate.reject("SPREAD_UNAVAILABLE")
            return candidate

        # ----------------------------
        # Negative/Invalid Volume
        # ----------------------------
        if candidate.volume < 0 or math.isnan(candidate.volume):
            candidate.reject("NEGATIVE_VOLUME")
            return candidate

        # ----------------------------
        # Negative/Invalid Open Interest
        # ----------------------------
        if candidate.open_interest < 0 or math.isnan(candidate.open_interest):
            candidate.reject("NEGATIVE_OPEN_INTEREST")
            return candidate

        # ----------------------------
        # NaN Greeks
        # ----------------------------
        if math.isnan(candidate.implied_volatility):
            candidate.reject("NAN_IMPLIED_VOLATILITY")
            return candidate
            
        candidate.state = "VALIDATED"
        return candidate

    def apply_all(self, candidates):
        accepted = []
        rejected = []
        seen_symbols = set()

        for candidate in candidates:
            # ----------------------------
            # Duplicate Candidate
            # ----------------------------
            if candidate.option_symbol in seen_symbols:
                candidate.reject("DUPLICATE_CANDIDATE")
                rejected.append(candidate)
                continue
                
            seen_symbols.add(candidate.option_symbol)
            candidate = self.apply(candidate)

            if candidate.execute is False and candidate.rejection_reason is not None:
                rejected.append(candidate)
            else:
                accepted.append(candidate)

        return accepted, rejected