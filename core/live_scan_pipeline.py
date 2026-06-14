"""
==========================================================

QuantEdge AI

Live Scan Pipeline

Flow

Universe
    ↓
History
    ↓
Features
    ↓
Option Chain
    ↓
Strike Selection
    ↓
Candidate Generation
    ↓
Filtering
    ↓
Ranking
    ↓
Decision

==========================================================
"""


class LiveScanPipeline:

    def __init__(

        self,

        universe_manager,

        data_engine,

        feature_engine,

        option_chain_parser,

        strike_selector,

        candidate_engine,

        filter_engine,

        ranking_engine,

        decision_engine,

    ):

        self.universe = universe_manager

        self.data = data_engine

        self.feature = feature_engine

        self.parser = option_chain_parser

        self.selector = strike_selector

        self.candidate = candidate_engine

        self.filter = filter_engine

        self.ranking = ranking_engine

        self.decision = decision_engine

    # ------------------------------------------------

    def run(

        self,

        resolution,

        start,

        end,

    ):

        all_candidates = []

        symbols = self.universe.get_all()

        for symbol in symbols:

            try:

                history = self.data.history(

                    symbol,

                    resolution,

                    start,

                    end,

                )

                if history is None:

                    continue

                history = self.feature.build(

                    history

                )

                feature_vector = self.feature.feature_vector(

                    history

                )

                raw_chain = self.data.option_chain(

                    symbol

                )

                if raw_chain is None:

                    continue

                chain = self.parser.parse(

                    raw_chain

                )

                calls = self.parser.calls(

                    chain

                )

                puts = self.parser.puts(

                    chain

                )

                selected = self.selector.select(

                    calls,

                    puts,

                )

                ce = selected["CE"]

                pe = selected["PE"]

                if ce is not None:

                    all_candidates.append(

                        self.candidate.create_candidate(

                            symbol=symbol,

                            direction="CE",

                            stock_price=feature_vector["close"],

                            option_symbol=ce["symbol"],

                            option_price=ce["ltp"],

                            strike=ce["strike"],

                            expiry="",

                            feature_vector=feature_vector,

                        )

                    )

                if pe is not None:

                    all_candidates.append(

                        self.candidate.create_candidate(

                            symbol=symbol,

                            direction="PE",

                            stock_price=feature_vector["close"],

                            option_symbol=pe["symbol"],

                            option_price=pe["ltp"],

                            strike=pe["strike"],

                            expiry="",

                            feature_vector=feature_vector,

                        )

                    )

            except Exception as e:

                print(

                    f"{symbol} skipped : {e}"

                )

                continue

        accepted, rejected = self.filter.apply_all(

            all_candidates

        )

        ranked = self.ranking.rank(

            accepted

        )

        decision = self.decision.decide(

            ranked

        )

        return {

            "decision": decision,

            "ranked": ranked,

            "accepted": accepted,

            "rejected": rejected,

            "total": len(symbols),

        }