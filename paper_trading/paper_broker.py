"""
==========================================================

QuantEdge AI

Paper Broker

Responsibilities
----------------
1. Simulate Buy Orders
2. Simulate Sell Orders
3. Track Cash
4. Track Positions
5. Track Trade History

==========================================================
"""

from datetime import datetime


class PaperBroker:

    def __init__(self, initial_capital=100000):

        self.initial_capital = initial_capital
        self.cash = initial_capital

        self.positions = {}

        self.trade_history = []

        self.order_number = 1

    # ------------------------------------------------

    def place_buy(

        self,

        symbol,

        price,

        quantity,

    ):

        cost = price * quantity

        if cost > self.cash:

            return {

                "success": False,

                "message": "INSUFFICIENT_FUNDS"

            }

        self.cash -= cost

        self.positions[symbol] = {

            "quantity": quantity,

            "entry_price": price,

            "entry_time": datetime.now()

        }

        order_id = f"PAPER-{self.order_number}"

        self.order_number += 1

        self.trade_history.append({

            "order_id": order_id,

            "type": "BUY",

            "symbol": symbol,

            "price": price,

            "quantity": quantity,

            "time": datetime.now()

        })

        return {

            "success": True,

            "order_id": order_id

        }

    # ------------------------------------------------

    def place_sell(

        self,

        symbol,

        price,

    ):

        if symbol not in self.positions:

            return {

                "success": False,

                "message": "POSITION_NOT_FOUND"

            }

        position = self.positions[symbol]

        quantity = position["quantity"]

        proceeds = quantity * price

        self.cash += proceeds

        pnl = (

            price -

            position["entry_price"]

        ) * quantity

        order_id = f"PAPER-{self.order_number}"

        self.order_number += 1

        self.trade_history.append({

            "order_id": order_id,

            "type": "SELL",

            "symbol": symbol,

            "price": price,

            "quantity": quantity,

            "pnl": pnl,

            "time": datetime.now()

        })

        del self.positions[symbol]

        return {

            "success": True,

            "order_id": order_id,

            "pnl": pnl

        }

    # ------------------------------------------------

    def portfolio_value(self):

        return self.cash

    # ------------------------------------------------

    def open_positions(self):

        return self.positions

    # ------------------------------------------------

    def history(self):

        return self.trade_history