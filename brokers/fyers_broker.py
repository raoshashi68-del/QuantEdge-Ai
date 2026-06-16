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

        fyers_symbol = symbol
        if not fyers_symbol.startswith("NSE:"):
            fyers_symbol = f"NSE:{symbol}-EQ"

        payload = {

            "symbol": fyers_symbol,

            "resolution": resolution,

            "date_format": "1",

            "range_from": start,

            "range_to": end,

            "cont_flag": "1"

        }

        raw = self.fyers.history(payload)

        import pandas as pd

        if isinstance(raw, dict):
            if raw.get("s") == "ok" and "candles" in raw:
                df = pd.DataFrame(raw["candles"], columns=["Datetime", "Open", "High", "Low", "Close", "Volume"])
                
                # Fyers timestamps are typically in epoch seconds
                df["Datetime"] = pd.to_datetime(df["Datetime"], unit="s")
                df = df.sort_values("Datetime", ascending=True)
                df = df.reset_index(drop=True)
                return df
            else:
                # API returned an error message or empty payload, raise it so it's visible in debug
                raise Exception(f"Fyers API Error: {raw}")

        return raw

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

    def option_chain(self, symbol):
        
        formatted_symbol = symbol
        if not symbol.startswith("NSE:"):
            formatted_symbol = f"NSE:{symbol}-EQ"

        payload = {
            "symbol": formatted_symbol,
            "strikecount": 5,
            "timestamp": ""
        }

        response = self.fyers.optionchain(payload)
        
        if response and response.get("s") == "ok" and response.get("data"):
            return response["data"].get("optionsChain", [])
            
        return []

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