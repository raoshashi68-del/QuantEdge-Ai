"""
==========================================================

QuantEdge AI

Backtester

Responsibilities
----------------
1. Replay historical data
2. Simulate entries
3. Simulate exits
4. Calculate statistics

==========================================================
"""

from dataclasses import dataclass
from typing import List


@dataclass
class BacktestResult:

    trades: int

    wins: int

    losses: int

    gross_profit: float

    gross_loss: float

    net_profit: float

    win_rate: float

    profit_factor: float


class Backtester:

    def __init__(self):

        self.history = []

    # ------------------------------------------------

    def record_trade(

        self,

        entry,

        exit,

        quantity,

    ):

        pnl = (exit - entry) * quantity

        self.history.append(pnl)

    # ------------------------------------------------

    def summary(self):

        trades = len(self.history)

        wins = sum(

            1

            for x in self.history

            if x > 0

        )

        losses = trades - wins

        gross_profit = sum(

            x

            for x in self.history

            if x > 0

        )

        gross_loss = abs(

            sum(

                x

                for x in self.history

                if x < 0

            )

        )

        net_profit = gross_profit - gross_loss

        if trades == 0:

            win_rate = 0

        else:

            win_rate = wins / trades * 100

        if gross_loss == 0:

            profit_factor = float("inf")

        else:

            profit_factor = gross_profit / gross_loss

        return BacktestResult(

            trades=trades,

            wins=wins,

            losses=losses,

            gross_profit=gross_profit,

            gross_loss=gross_loss,

            net_profit=net_profit,

            win_rate=win_rate,

            profit_factor=profit_factor,

        )