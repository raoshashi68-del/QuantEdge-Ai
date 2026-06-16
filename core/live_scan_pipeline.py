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
        
        evidence_engine=None,
        
        probability_engine=None,
        
        expected_return_engine=None,

        risk_engine=None,
        
        expected_value_engine=None,
        
        confidence_engine=None,
        
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
        
        self.evidence = evidence_engine
        
        self.probability = probability_engine
        
        self.expected_return = expected_return_engine
        
        self.risk = risk_engine
        
        self.expected_value = expected_value_engine
        
        self.confidence = confidence_engine

    # ------------------------------------------------

    def run(

        self,

        resolution,

        start,

        end,

    ):

        all_candidates = []

        symbols = self.universe.get_all()

        print(f"Universe:\n{len(symbols)}\n")
        
        if len(symbols) == 0:
            print("STOPPING AT STAGE: Universe")
            print("Rejection reason: UniverseManager returned empty list")
            return {"decision": None, "ranked": [], "accepted": [], "rejected": [], "total": 0}

        history_count = 0
        features_count = 0
        chain_count = 0
        strike_selected_count = 0
        
        history_rejections = []
        feature_rejections = []
        chain_rejections = []
        strike_rejections = []

        for symbol in symbols:

            try:

                history = self.data.history(

                    symbol,

                    resolution,

                    start,

                    end,

                )

                if history is None:
                    history_rejections.append(f"{symbol}: History returned None")
                    continue
                history_count += 1

                try:
                    history = self.feature.build(history)
                    feature_vector = self.feature.feature_vector(history)
                    features_count += 1
                except Exception as e:
                    feature_rejections.append(f"{symbol}: Feature engine error - {e}")
                    continue

                raw_chain = self.data.option_chain(symbol)

                if raw_chain is None:
                    chain_rejections.append(f"{symbol}: Option chain returned None")
                    continue
                chain_count += 1

                chain = self.parser.parse(raw_chain)

                calls = self.parser.calls(chain)

                puts = self.parser.puts(chain)

                selected = self.selector.select(calls, puts)

                ce = selected.get("CE")

                pe = selected.get("PE")

                if ce is not None or pe is not None:
                    strike_selected_count += 1
                else:
                    strike_rejections.append(f"{symbol}: No CE or PE strikes selected")

                if ce is not None:

                    all_candidates.append(

                        self.candidate.create_candidate(
                            symbol=symbol,
                            direction="CE",
                            stock_price=feature_vector["close"],
                            option_symbol=ce["symbol"],
                            option_price=ce["ltp"],
                            strike=ce["strike"],
                            expiry="2026-06-19",
                            feature_vector=feature_vector,
                            volume=ce["volume"],
                            open_interest=ce["open_interest"],
                            bid=ce["bid"],
                            ask=ce["ask"],
                            spread_percent=ce["spread_percent"],
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
                            expiry="2026-06-19",
                            feature_vector=feature_vector,
                            volume=pe["volume"],
                            open_interest=pe["open_interest"],
                            bid=pe["bid"],
                            ask=pe["ask"],
                            spread_percent=pe["spread_percent"],
                        )

                    )

            except Exception as e:

                print(

                    f"{symbol} skipped : {e}"

                )

                continue

        print(f"History Loaded:\n{history_count}\n")
        if history_count == 0:
            print("STOPPING AT STAGE: History")
            print(f"Rejection reasons: {history_rejections[:3]}")
            return {"decision": None, "ranked": [], "accepted": [], "rejected": [], "total": len(symbols)}
            
        print(f"Features Generated:\n{features_count}\n")
        if features_count == 0:
            print("STOPPING AT STAGE: Features")
            print(f"Rejection reasons: {feature_rejections[:3]}")
            return {"decision": None, "ranked": [], "accepted": [], "rejected": [], "total": len(symbols)}

        print(f"Option Chains:\n{chain_count}\n")
        if chain_count == 0:
            print("STOPPING AT STAGE: Option Chains")
            print(f"Rejection reasons: {chain_rejections[:3]}")
            return {"decision": None, "ranked": [], "accepted": [], "rejected": [], "total": len(symbols)}

        print(f"Strike Selected:\n{strike_selected_count}\n")
        if strike_selected_count == 0:
            print("STOPPING AT STAGE: Strike Selection")
            print(f"Rejection reasons: {strike_rejections[:3]}")
            return {"decision": None, "ranked": [], "accepted": [], "rejected": [], "total": len(symbols)}

        print(f"Candidates Generated:\n{len(all_candidates)}\n")
        if len(all_candidates) == 0:
            print("STOPPING AT STAGE: Candidate Generation")
            print("Rejection reasons: No valid candidates created from strikes")
            return {"decision": None, "ranked": [], "accepted": [], "rejected": [], "total": len(symbols)}
            
        # [STAGE 7] Execution Validation Layer (formerly FilterEngine)
        accepted_candidates, rejected_candidates = self.filter.apply_all(all_candidates)
        
        print(f"Candidates After Validation:\n{len(accepted_candidates)}\n")
        if len(accepted_candidates) == 0:
            print("STOPPING AT STAGE: Execution Validation")
            print(f"Rejection reasons: {[c.rejection_reason for c in rejected_candidates[:3]]}")
            return {"decision": None, "ranked": [], "accepted": [], "rejected": rejected_candidates, "total": len(symbols)}
            
        # [STAGE 1-6] Core Math Engines Integration
        if self.evidence:
            for c in accepted_candidates:
                c.evidence = self.evidence.build(c.features, c)
                if self.probability:
                    c.probability_result = self.probability.build(c.evidence)
                if self.expected_return:
                    c.expected_return_result = self.expected_return.build(c.evidence)
                if self.risk:
                    c.risk_result = self.risk.build(c.evidence)
                if self.expected_value and self.probability and self.expected_return and self.risk:
                    c.expected_value_result = self.expected_value.build(
                        c.probability_result,
                        c.expected_return_result,
                        c.risk_result
                    )
                if self.confidence and self.probability and self.expected_return and self.risk:
                    c.confidence_result = self.confidence.build(
                        c.evidence,
                        c.probability_result,
                        c.expected_return_result,
                        c.risk_result
                    )

        accepted = accepted_candidates
        rejected = rejected_candidates

        ranked = self.ranking.rank(

            accepted

        )

        print(f"Candidates Ranked:\n{len(ranked)}\n")
        if len(ranked) == 0:
            print("STOPPING AT STAGE: Ranking")
            print("Rejection reasons: Ranking dropped all candidates")
            return {"decision": None, "ranked": [], "accepted": accepted, "rejected": rejected, "total": len(symbols)}

        decision = self.decision.decide(

            ranked

        )
        
        decision_str = "EXECUTE" if decision and getattr(decision, "action", "") == "EXECUTE" else "NO_TRADE"
        print(f"Decision:\n{decision_str}\n")

        return {

            "decision": decision,

            "ranked": ranked,

            "accepted": accepted,

            "rejected": rejected,

            "total": len(symbols),

        }