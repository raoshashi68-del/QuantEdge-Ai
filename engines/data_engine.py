"""
==========================================================
QuantEdge AI

Data Engine

Responsibilities
----------------
1. Fetch Historical Data
2. Fetch Live Quotes
3. Cache Results
4. Retry Failed Requests
5. Return Standardized DataFrame

==========================================================
"""

from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from datetime import datetime
import time

import pandas as pd

from config.settings import MAX_WORKERS


class DataEngine:

    def __init__(self, broker):

        self.broker = broker

        self.cache = {}

        self.cache_time = {}

        self.lock = Lock()

    # ----------------------------------------------------
    # Cache
    # ----------------------------------------------------

    def _get_cache(self, key, expiry):

        with self.lock:

            if key not in self.cache:

                return None

            age = time.time() - self.cache_time[key]

            if age > expiry:

                del self.cache[key]

                del self.cache_time[key]

                return None

            return self.cache[key]

    def _set_cache(self, key, value):

        with self.lock:

            self.cache[key] = value

            self.cache_time[key] = time.time()

    # ----------------------------------------------------
    # Validation
    # ----------------------------------------------------

    @staticmethod
    def validate(df):

        required = [

            "Open",

            "High",

            "Low",

            "Close",

            "Volume"

        ]

        if df is None:

            return False

        for col in required:

            if col not in df.columns:

                return False

        return True

    # ----------------------------------------------------
    # Normalize
    # ----------------------------------------------------

    @staticmethod
    def normalize(df):

        df = df.copy()

        df.columns = [

            c.capitalize()

            for c in df.columns

        ]

        if "Datetime" not in df.columns:

            if "Timestamp" in df.columns:

                df.rename(

                    columns={

                        "Timestamp":"Datetime"

                    },

                    inplace=True

                )

        if "Datetime" in df.columns:
            df["Datetime"] = pd.to_datetime(
                df["Datetime"]
            )
            df.set_index(
                "Datetime",
                inplace=True
            )

        # QuantEdge Data Contract v1.0
        df = df.sort_index()
        df = df[~df.index.duplicated(keep="last")]

        assert df.index.is_unique, "Data Contract Violation: Index not unique"
        assert df.columns.is_unique, "Data Contract Violation: Columns not unique"
        assert df.index.is_monotonic_increasing, "Data Contract Violation: Index not monotonic increasing"
        assert {"Open", "High", "Low", "Close", "Volume"} <= set(df.columns), "Data Contract Violation: Missing OHLCV columns"

        return df

    # ----------------------------------------------------
    # History
    # ----------------------------------------------------

    def history(

        self,

        symbol,

        resolution,

        start,

        end,

        cache_seconds=30,

    ):

        print("\n==========================")
        print("DATAENGINE HISTORY DEBUG")
        print("==========================")
        print("Symbol:")
        print(symbol)
        print("Arguments:")
        print(f"resolution={resolution}, start={start}, end={end}")
        print("Provider:")
        print(self.broker.__class__.__name__)
        print("Fetching...")

        try:

            df = self.broker.history(

                symbol,

                resolution,

                start,

                end

            )

        except Exception as e:
            print("Exception:")
            import traceback
            traceback.print_exc()
            print(e)
            raise

        print("Result Type:")
        print(type(df))
        print("Is None:")
        print(df is None)
        print("Length:")
        try:
            print(len(df))
        except:
            print("N/A")

        df = self.normalize(df)

        if self.validate(df):

            return df

        return None

    # ----------------------------------------------------
    # Quote
    # ----------------------------------------------------

    def quote(

        self,

        symbol,

        cache_seconds=2,

    ):

        key = ("QUOTE", symbol)

        cached = self._get_cache(

            key,

            cache_seconds

        )

        if cached is not None:

            return cached

        for _ in range(3):

            try:

                q = self.broker.quote(

                    symbol

                )

                self._set_cache(

                    key,

                    q

                )

                return q

            except Exception:

                time.sleep(0.5)

                continue

        return None

    # ----------------------------------------------------
    # Option Chain
    # ----------------------------------------------------

    def option_chain(

        self,

        symbol,

        cache_seconds=5,

    ):

        key = (

            "CHAIN",

            symbol

        )

        cached = self._get_cache(

            key,

            cache_seconds

        )

        if cached is not None:

            return cached

        chain = self.broker.option_chain(

            symbol

        )

        self._set_cache(

            key,

            chain

        )

        return chain

    # ----------------------------------------------------
    # Parallel Quotes
    # ----------------------------------------------------

    def quotes(

        self,

        symbols,

    ):

        result = {}

        def worker(sym):

            return (

                sym,

                self.quote(sym)

            )

        with ThreadPoolExecutor(

            max_workers=MAX_WORKERS

        ) as executor:

            futures = [

                executor.submit(

                    worker,

                    s

                )

                for s in symbols

            ]

            for future in futures:

                sym, q = future.result()

                result[sym] = q

        return result

    # ----------------------------------------------------
    # Parallel History
    # ----------------------------------------------------

    def histories(

        self,

        symbols,

        resolution,

        start,

        end,

    ):

        result = {}

        def worker(sym):

            return (

                sym,

                self.history(

                    sym,

                    resolution,

                    start,

                    end

                )

            )

        with ThreadPoolExecutor(

            max_workers=MAX_WORKERS

        ) as executor:

            futures = [

                executor.submit(

                    worker,

                    s

                )

                for s in symbols

            ]

            for future in futures:

                sym, df = future.result()

                result[sym] = df

        return result