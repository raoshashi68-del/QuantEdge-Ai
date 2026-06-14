"""
==========================================================

QuantEdge AI

Fyers Broker Adapter

Responsibilities
----------------
1. Historical data
2. Live quote
3. Option chain
4. Place order
5. Positions
6. Orders

==========================================================
"""

from fyers_apiv3 import fyersModel


class FyersBroker:

    def __init__(

        self,

        client_id,

        access_token,

    ):

        self.fyers = fyersModel.FyersModel(

            client_id=client_id,

            token=access_token,

            is_async=False,

            log_path=""

        )

    # -------------------------------------------------

    def history(

        self,

        symbol,

        resolution,

        start,

        end,

    ):

        payload = {

            "symbol": symbol,

            "resolution": resolution,

            "date_format": "1",

            "range_from": start,

            "range_to": end,

            "cont_flag": "1"

        }

        return self.fyers.history(payload)

    # -------------------------------------------------

    def quote(

        self,

        symbol,

    ):

        payload = {

            "symbols": symbol

        }

        return self.fyers.quotes(payload)

    # -------------------------------------------------

    def option_chain(

        self,

        symbol,

    ):

        payload = {

            "symbol": symbol

        }

        return self.fyers.optionchain(payload)

    # -------------------------------------------------

    def place_order(

        self,

        symbol,

        side,

        quantity,

        order_type="MARKET",

        product="INTRADAY",

    ):

        payload = {

            "symbol": symbol,

            "qty": quantity,

            "type": 2 if order_type == "MARKET" else 1,

            "side": 1 if side == "BUY" else -1,

            "productType": product,

            "validity": "DAY",

            "offlineOrder": False

        }

        return self.fyers.place_order(payload)

    # -------------------------------------------------

    def positions(self):

        return self.fyers.positions()

    # -------------------------------------------------

    def orders(self):

        return self.fyers.orderbook()