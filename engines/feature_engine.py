"""
==========================================================

QuantEdge AI

Feature Engine

Responsibilities
----------------
1. Calculate indicators
2. Generate feature vector
3. NO decisions
4. NO scoring

==========================================================
"""

import pandas as pd
import pandas_ta as ta


class FeatureEngine:

    def __init__(self):
        pass

    # --------------------------------------------------
    # Relative Volume
    # --------------------------------------------------

    @staticmethod
    def relative_volume(df, period=20):

        avg = df["Volume"].rolling(period).mean()

        return df["Volume"] / avg

    # --------------------------------------------------
    # Opening Range High
    # --------------------------------------------------

    @staticmethod
    def opening_range_high(df, candles=3):

        return df["High"].iloc[:candles].max()

    # --------------------------------------------------
    # Opening Range Low
    # --------------------------------------------------

    @staticmethod
    def opening_range_low(df, candles=3):

        return df["Low"].iloc[:candles].min()

    # --------------------------------------------------
    # Feature Extraction
    # --------------------------------------------------

    def build(self, df):

        if df is None:

            return None

        df = df.copy()

        # EMA

        df["EMA9"] = ta.ema(
            df["Close"],
            length=9
        )

        df["EMA20"] = ta.ema(
            df["Close"],
            length=20
        )

        df["EMA50"] = ta.ema(
            df["Close"],
            length=50
        )

        # RSI

        df["RSI"] = ta.rsi(
            df["Close"],
            length=14
        )

        # ATR

        df["ATR"] = ta.atr(
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            length=14
        )

        # ADX

        adx = ta.adx(
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            length=14
        )

        df["ADX"] = adx.iloc[:, 0]

        # MACD

        macd = ta.macd(df["Close"])

        df["MACD"] = macd.iloc[:, 0]

        df["MACD_SIGNAL"] = macd.iloc[:, 1]

        df["MACD_HIST"] = macd.iloc[:, 2]

        # Supertrend

        st = ta.supertrend(
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            length=10,
            multiplier=3
        )

        df["SUPERTREND"] = st.iloc[:, 0]

        df["SUPERTREND_DIRECTION"] = st.iloc[:, 1]

        # VWAP

        df["VWAP"] = ta.vwap(
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            volume=df["Volume"]
        )

        # Relative Volume

        df["REL_VOLUME"] = self.relative_volume(df)

        # Opening Range

        orb_high = self.opening_range_high(df)

        orb_low = self.opening_range_low(df)

        df["ORB_HIGH"] = orb_high

        df["ORB_LOW"] = orb_low

        return df

    # --------------------------------------------------
    # Latest Feature Vector
    # --------------------------------------------------

    def feature_vector(self, df):

        row = df.iloc[-1]

        return {

            "close": row["Close"],

            "ema9": row["EMA9"],

            "ema20": row["EMA20"],

            "ema50": row["EMA50"],

            "rsi": row["RSI"],

            "atr": row["ATR"],

            "adx": row["ADX"],

            "macd": row["MACD"],

            "macd_signal": row["MACD_SIGNAL"],

            "macd_hist": row["MACD_HIST"],

            "supertrend": row["SUPERTREND"],

            "supertrend_direction":
                row["SUPERTREND_DIRECTION"],

            "vwap": row["VWAP"],

            "relative_volume":
                row["REL_VOLUME"],

            "orb_high":
                row["ORB_HIGH"],

            "orb_low":
                row["ORB_LOW"]

        }