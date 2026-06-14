"""
=========================================

Broker Interface

=========================================
"""

from abc import ABC, abstractmethod


class Broker(ABC):

    @abstractmethod
    def history(
        self,
        symbol,
        resolution,
        start,
        end,
    ):
        pass

    @abstractmethod
    def quote(
        self,
        symbol,
    ):
        pass

    @abstractmethod
    def option_chain(
        self,
        symbol,
    ):
        pass

    @abstractmethod
    def place_order(
        self,
        **kwargs,
    ):
        pass

    @abstractmethod
    def positions(self):
        pass

    @abstractmethod
    def orders(self):
        pass