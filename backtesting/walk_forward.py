"""
==========================================================

QuantEdge AI

Walk Forward Backtester

Responsibilities
----------------
1. Split data into Train/Test windows
2. Execute strategy on each window
3. Record metrics
4. Return overall performance

==========================================================
"""

from dataclasses import dataclass


@dataclass
class WalkForwardResult:

    windows: int

    total_trades: int

    net_profit: float

    average_profit: float

    win_rate: float


class WalkForward:

    def __init__(

        self,

        strategy,

        train_size=100,

        test_size=20,

    ):

        self.strategy = strategy

        self.train_size = train_size

        self.test_size = test_size

    # ------------------------------------------------

    def run(

        self,

        data,

    ):

        index = 0

        total_profit = 0

        total_trades = 0

        total_wins = 0

        windows = 0

        while (

            index +

            self.train_size +

            self.test_size

            <=

            len(data)

        ):

            train = data[

                index:

                index +

                self.train_size

            ]

            test = data[

                index +

                self.train_size:

                index +

                self.train_size +

                self.test_size

            ]

            self.strategy.fit(train)

            trades = self.strategy.test(test)

            for pnl in trades:

                total_profit += pnl

                total_trades += 1

                if pnl > 0:

                    total_wins += 1

            windows += 1

            index += self.test_size

        average_profit = 0

        if total_trades > 0:

            average_profit = (

                total_profit /

                total_trades

            )

        win_rate = 0

        if total_trades > 0:

            win_rate = (

                total_wins *

                100 /

                total_trades

            )

        return WalkForwardResult(

            windows=windows,

            total_trades=total_trades,

            net_profit=total_profit,

            average_profit=average_profit,

            win_rate=win_rate,

        )