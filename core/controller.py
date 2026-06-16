"""
==========================================================

QuantEdge AI

Controller

Responsibilities
----------------
1. Run one complete scan cycle
2. Build candidates
3. Filter candidates
4. Rank candidates
5. Make decision

==========================================================
"""


class Controller:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self, resolution="1", start="", end=""):
        import datetime
        if not start or not end:
            today = datetime.date.today()
            start_date = today - datetime.timedelta(days=30)
            start = start_date.strftime("%Y-%m-%d")
            end = today.strftime("%Y-%m-%d")
            
        return self.pipeline.run(
            resolution=resolution,
            start=start,
            end=end
        )