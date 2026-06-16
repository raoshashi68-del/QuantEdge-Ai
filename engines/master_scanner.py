"""
==========================================================

QuantEdge AI

Master Scanner

==========================================================
"""

from concurrent.futures import ThreadPoolExecutor
from config.settings import MAX_WORKERS


class MasterScanner:

    def __init__(

        self,

        pipeline=None,
        **kwargs

    ):

        self.pipeline = pipeline
        for k, v in kwargs.items():
            setattr(self, k, v)

    # -----------------------------------------

    def scan_symbol(

        self,

        symbol,

        resolution,

        start,

        end,

    ):

        try:
            if not self.pipeline:
                return []

            return self.pipeline.scan_symbol(

                symbol=symbol,

                resolution=resolution,

                start=start,

                end=end,

            )

        except Exception:

            return []

    # -----------------------------------------

    def scan(

        self,

        universe=None,

        resolution="1",

        start="",

        end="",

    ):
        if universe is None:
            universe = []

        candidates = []

        with ThreadPoolExecutor(

            max_workers=MAX_WORKERS

        ) as executor:

            futures = [

                executor.submit(

                    self.scan_symbol,

                    symbol,

                    resolution,

                    start,

                    end,

                )

                for symbol in universe

            ]

            for future in futures:

                result = future.result()

                if result:

                    candidates.extend(result)

        return candidates