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

        pipeline,

    ):

        self.pipeline = pipeline

    # -----------------------------------------

    def scan_symbol(

        self,

        symbol,

        resolution,

        start,

        end,

    ):

        try:

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

        universe,

        resolution,

        start,

        end,

    ):

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