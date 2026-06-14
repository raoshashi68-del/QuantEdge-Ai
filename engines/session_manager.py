"""
==========================================================

QuantEdge AI

Session Manager

Responsibilities
----------------
1. Check market status
2. Check entry window
3. Check exit window
4. Control scan timing

==========================================================
"""

from datetime import datetime, time


class SessionManager:

    def __init__(

        self,

        market_open="09:15",

        market_close="15:30",

        last_entry="15:00",

        force_exit="15:15",

    ):

        self.market_open = self._to_time(market_open)

        self.market_close = self._to_time(market_close)

        self.last_entry = self._to_time(last_entry)

        self.force_exit = self._to_time(force_exit)

    # ------------------------------------------------

    @staticmethod
    def _to_time(value):

        h, m = value.split(":")

        return time(

            int(h),

            int(m)

        )

    # ------------------------------------------------

    @staticmethod
    def now():

        return datetime.now().time()

    # ------------------------------------------------

    def is_market_open(self):

        t = self.now()

        return (

            self.market_open

            <=

            t

            <=

            self.market_close

        )

    # ------------------------------------------------

    def can_enter_trade(self):

        t = self.now()

        return (

            self.market_open

            <=

            t

            <=

            self.last_entry

        )

    # ------------------------------------------------

    def should_force_exit(self):

        t = self.now()

        return (

            t

            >=

            self.force_exit

        )

    # ------------------------------------------------

    def status(self):

        if not self.is_market_open():

            return "MARKET_CLOSED"

        if self.should_force_exit():

            return "FORCE_EXIT"

        if self.can_enter_trade():

            return "ENTRY_ALLOWED"

        return "NO_NEW_ENTRY"