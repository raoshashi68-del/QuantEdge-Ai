"""
==========================================================

QuantEdge AI

Universe Manager

Responsibilities
----------------
1. Load trading universe
2. Remove duplicates
3. Enable/disable symbols
4. Return active universe

==========================================================
"""

from typing import List


class UniverseManager:

    def __init__(self):

        self._symbols = []

    # ----------------------------------------

    def add(self, symbol: str):

        symbol = symbol.strip().upper()

        if symbol not in self._symbols:

            self._symbols.append(symbol)

    # ----------------------------------------

    def add_many(self, symbols: List[str]):

        for symbol in symbols:

            self.add(symbol)

    # ----------------------------------------

    def remove(self, symbol: str):

        symbol = symbol.strip().upper()

        if symbol in self._symbols:

            self._symbols.remove(symbol)

    # ----------------------------------------

    def clear(self):

        self._symbols.clear()

    # ----------------------------------------

    def get_all(self):

        return list(self._symbols)

    # ----------------------------------------

    def count(self):

        return len(self._symbols)

    # ----------------------------------------

    def contains(self, symbol):

        return symbol.strip().upper() in self._symbols