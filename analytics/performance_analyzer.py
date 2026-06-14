"""
==========================================================

QuantEdge AI

Performance Analyzer

Responsibilities
----------------
1. Total Trades
2. Win Rate
3. Net Profit
4. Average Profit
5. Average Loss
6. Profit Factor
7. Max Drawdown

==========================================================
"""

from dataclasses import dataclass


@dataclass
class PerformanceSummary:

    total_trades: int

    winning_trades: int

    losing_trades: int

    win_rate: float

    gross_profit: float

    gross_loss: float

    net_profit: float

    average_profit: float

    average_loss: float

    profit_factor: float

    max_drawdown: float


class PerformanceAnalyzer:

    def __init__(self):

        self.trades = []

    # ------------------------------------------------

    def add_trade(self, pnl):

        self.trades.append(float(pnl))

    # ------------------------------------------------

    def analyze(self):

        total = len(self.trades)

        wins = [x for x in self.trades if x > 0]

        losses = [x for x in self.trades if x < 0]

        winning_trades = len(wins)

        losing_trades = len(losses)

        gross_profit = sum(wins)

        gross_loss = abs(sum(losses))

        net_profit = gross_profit - gross_loss

        win_rate = 0.0

        if total > 0:

            win_rate = winning_trades * 100 / total

        average_profit = 0.0

        if winning_trades > 0:

            average_profit = gross_profit / winning_trades

        average_loss = 0.0

        if losing_trades > 0:

            average_loss = gross_loss / losing_trades

        if gross_loss == 0:

            profit_factor = float("inf")

        else:

            profit_factor = gross_profit / gross_loss

        max_drawdown = self.calculate_drawdown()

        return PerformanceSummary(

            total_trades=total,

            winning_trades=winning_trades,

            losing_trades=losing_trades,

            win_rate=win_rate,

            gross_profit=gross_profit,

            gross_loss=gross_loss,

            net_profit=net_profit,

            average_profit=average_profit,

            average_loss=average_loss,

            profit_factor=profit_factor,

            max_drawdown=max_drawdown,

        )

    # ------------------------------------------------

    def calculate_drawdown(self):

        equity = 0

        peak = 0

        max_dd = 0

        for pnl in self.trades:

            equity += pnl

            if equity > peak:

                peak = equity

            dd = peak - equity

            if dd > max_dd:

                max_dd = dd

        return max_dd