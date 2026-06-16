"""
==========================================================
QuantEdge AI
Evidence Engine
==========================================================
"""

import math
from models.evidence_vector import EvidenceVector

class EvidenceEngine:
    def __init__(self):
        pass

    def score_trend(self, feature_vector) -> float:
        close = feature_vector.get("close", 0)
        ema9 = feature_vector.get("ema9", close)
        ema20 = feature_vector.get("ema20", close)
        ema50 = feature_vector.get("ema50", close)
        
        score = 50.0
        if close > ema9 and ema9 > ema20 and ema20 > ema50:
            score = 90.0
        elif close < ema9 and ema9 < ema20 and ema20 < ema50:
            score = 10.0
            
        adx = feature_vector.get("adx", 0)
        if adx > 25:
            if score > 50:
                score = min(100.0, score + 10)
            elif score < 50:
                score = max(0.0, score - 10)
        return score

    def score_momentum(self, feature_vector) -> float:
        rsi = feature_vector.get("rsi", 50)
        score = float(rsi)
        
        macd_hist = feature_vector.get("macd_hist", 0)
        if macd_hist > 0:
            score = min(100.0, score + 10)
        elif macd_hist < 0:
            score = max(0.0, score - 10)
            
        return score

    def score_volume(self, feature_vector) -> float:
        rvol = feature_vector.get("relative_volume", 1.0)
        score = min(100.0, max(0.0, rvol * 50.0))
        return score

    def score_volatility(self, feature_vector) -> float:
        atr = feature_vector.get("atr", 0)
        close = feature_vector.get("close", 1)
        if close == 0:
            return 50.0
        atr_pct = (atr / close) * 100
        score = min(100.0, max(0.0, atr_pct * 50.0))
        return score

    def score_structure(self, feature_vector) -> float:
        close = feature_vector.get("close", 0)
        orb_high = feature_vector.get("orb_high", close)
        orb_low = feature_vector.get("orb_low", close)
        
        if orb_high == orb_low:
            return 50.0
            
        position = (close - orb_low) / (orb_high - orb_low) if orb_high > orb_low else 0.5
        score = position * 100.0
        return min(100.0, max(0.0, score))

    def score_execution(self, candidate) -> float:
        spread = candidate.spread
        spread_score = max(0.0, 100.0 - (spread * 50.0))
        
        oi = candidate.open_interest
        oi_score = min(100.0, (oi / 100000.0) * 100.0)
        
        vol = candidate.volume
        vol_score = min(100.0, (vol / 50000.0) * 100.0)
        
        score = (spread_score * 0.5) + (oi_score * 0.25) + (vol_score * 0.25)
        return min(100.0, max(0.0, score))

    def score_consistency(self, trend, momentum, volume, structure) -> float:
        scores = [trend, momentum, volume, structure]
        mean = sum(scores) / len(scores)
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)
        std_dev = math.sqrt(variance)
        
        # Max theoretical std_dev is 50.
        # So consistency ranges from 100 (identical scores) to 0 (highly contradictory).
        consistency = max(0.0, 100.0 - (std_dev * 2.0))
        return consistency

    def institutional_score(self, trend, momentum, volume, volatility, structure, execution, consistency) -> float:
        directional_quality = (trend + momentum + structure) / 3.0
        opportunity_quality = (volume + volatility + execution) / 3.0
        
        score = (directional_quality / 100.0) * (opportunity_quality / 100.0) * (consistency / 100.0) * 100.0
        
        return min(100.0, max(0.0, score))

    def build(self, feature_vector, candidate) -> EvidenceVector:
        trend = self.score_trend(feature_vector)
        momentum = self.score_momentum(feature_vector)
        volume = self.score_volume(feature_vector)
        volatility = self.score_volatility(feature_vector)
        structure = self.score_structure(feature_vector)
        execution = self.score_execution(candidate)
        consistency = self.score_consistency(trend, momentum, volume, structure)
        
        score = self.institutional_score(
            trend, momentum, volume, volatility, structure, execution, consistency
        )
        
        reasons = []
        warnings = []
        
        if trend > 75:
            reasons.append("+ EMA stack aligned and trending")
        elif trend < 25:
            warnings.append("- Trend is strongly bearish")
        else:
            warnings.append("- Neutral or conflicting trend")
            
        if momentum > 75:
            reasons.append("+ Momentum is accelerating")
        elif momentum < 25:
            warnings.append("- Momentum is weak or fading")
        else:
            warnings.append("- Momentum is neutral")
            
        if volume > 75:
            reasons.append("+ High relative volume confirms move")
        elif volume < 40:
            warnings.append("- Volume is weak")
        else:
            warnings.append("- Average participation")
            
        if volatility > 75:
            reasons.append("+ Healthy volatility expansion")
        elif volatility < 40:
            warnings.append("- ATR is contracting")
        else:
            reasons.append("+ Volatility is within normal bounds")
            
        if execution > 75:
            reasons.append("+ Liquidity and spread are optimal")
        elif execution < 50:
            warnings.append("- Execution risk: Wide spread or low liquidity")
        else:
            warnings.append("- Execution quality acceptable but not ideal")
            
        if structure > 75:
            reasons.append("+ Price holding above structural range")
        elif structure < 25:
            warnings.append("- Price failing at structural support")
        else:
            warnings.append("- Price inside structural range")
            
        if consistency < 40:
            warnings.append("- High contradiction between evidence indicators")
        elif consistency > 80:
            reasons.append("+ High consistency across indicators")
        
        vector = EvidenceVector(
            trend=trend,
            momentum=momentum,
            volume=volume,
            volatility=volatility,
            structure=structure,
            execution=execution,
            consistency=consistency,
            institutional_score=score,
            reasons=reasons,
            warnings=warnings,
            metadata={}
        )
        
        return vector
