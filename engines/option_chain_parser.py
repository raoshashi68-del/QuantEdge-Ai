"""
==========================================================

QuantEdge AI

Option Chain Parser

Responsibilities
----------------
1. Parse broker response
2. Standardize fields
3. Separate CE and PE
4. Return normalized options

==========================================================
"""

from typing import List, Dict


class OptionChainParser:

    REQUIRED_FIELDS = [
        "symbol",
        "type",
        "strike",
        "ltp",
        "volume",
        "open_interest",
        "bid",
        "ask",
    ]

    @staticmethod
    def spread_percent(bid, ask):

        if bid <= 0 or ask <= 0:
            return 100.0

        mid = (bid + ask) / 2

        if mid == 0:
            return 100.0

        return ((ask - bid) / mid) * 100

    @classmethod
    def normalize_option(cls, option: Dict):

        bid = float(option.get("bid", 0))
        ask = float(option.get("ask", 0))

        return {

            "symbol":
                option.get("symbol"),

            "type":
                option.get("type"),

            "strike":
                float(option.get("strike", 0)),

            "ltp":
                float(option.get("ltp", 0)),

            "volume":
                int(option.get("volume", 0)),

            "open_interest":
                int(option.get("open_interest", 0)),

            "bid":
                bid,

            "ask":
                ask,

            "spread_percent":
                cls.spread_percent(
                    bid,
                    ask,
                ),

        }

    @classmethod
    def parse(cls, raw_chain: List[Dict]):

        normalized = []

        for option in raw_chain:

            normalized.append(

                cls.normalize_option(
                    option
                )

            )

        return normalized

    @staticmethod
    def calls(chain):

        return [

            x

            for x in chain

            if x["type"] == "CE"

        ]

    @staticmethod
    def puts(chain):

        return [

            x

            for x in chain

            if x["type"] == "PE"

        ]