"""
==========================================================
QuantEdge AI
Data Provider Interface
==========================================================
"""

from abc import ABC, abstractmethod

class DataProvider(ABC):
    
    @abstractmethod
    def set_timestamp(self, current_time):
        """
        Set the internal clock for point-in-time abstractions.
        For backtesting, this strictly bounds the data returned.
        For live, this may just sync to system time.
        """
        pass
        
    @abstractmethod
    def history(self, symbol, resolution, start, end):
        """
        Return history strictly up to the internal timestamp
        to prevent forward-looking bias.
        """
        pass
        
    @abstractmethod
    def quote(self, symbol):
        """
        Return current quote exactly at the internal timestamp.
        """
        pass
        
    @abstractmethod
    def option_chain(self, symbol):
        """
        Return option chain exactly at the internal timestamp.
        """
        pass
