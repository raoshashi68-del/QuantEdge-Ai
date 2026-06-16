"""
==========================================================

QuantEdge AI

Candidate Engine

Responsibilities

1. Generate CE candidate

2. Generate PE candidate

3. Attach feature vector

4. Return TradeCandidate objects

==========================================================
"""

from models.trade_candidate import TradeCandidate


class CandidateEngine:

    def __init__(self):
        pass

    def create_candidate(
        self,
        symbol,
        direction,
        stock_price,
        option_symbol,
        option_price,
        strike,
        expiry,
        feature_vector,
        volume,
        open_interest,
        bid,
        ask,
        spread_percent,
    ):

        candidate = TradeCandidate(
            symbol=symbol,
            direction=direction,
            option_symbol=option_symbol,
            stock_price=stock_price,
            option_price=option_price,
            strike=strike,
            expiry=expiry,
            volume=volume,
            open_interest=open_interest,
            bid=bid,
            ask=ask,
            spread=spread_percent,
        )

        for key, value in feature_vector.items():

            candidate.add_feature(

                key,

                value,

            )

        return candidate

    def create_pair(

        self,

        symbol,

        stock_price,

        ce_symbol,

        ce_price,

        pe_symbol,

        pe_price,

        strike,

        expiry,

        feature_vector,

    ):

        ce = self.create_candidate(

            symbol,

            "CE",

            stock_price,

            ce_symbol,

            ce_price,

            strike,

            expiry,

            feature_vector,

        )

        pe = self.create_candidate(

            symbol,

            "PE",

            stock_price,

            pe_symbol,

            pe_price,

            strike,

            expiry,

            feature_vector,

        )

        return ce, pe