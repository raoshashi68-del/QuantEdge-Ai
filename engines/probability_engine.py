"""
==========================================================
QuantEdge AI
Probability Engine
==========================================================
"""

import math
from models.evidence_vector import EvidenceVector
from models.probability_result import ProbabilityResult

class ProbabilityEngine:
    def __init__(self):
        pass

    def build(self, evidence: EvidenceVector) -> ProbabilityResult:
        
        # 1. Component Qualities (0.0 to 1.0)
        directional_quality = (
            (evidence.trend * 0.5) + 
            (evidence.momentum * 0.3) + 
            (evidence.structure * 0.2)
        ) / 100.0
        
        opportunity_quality = (
            (evidence.execution * 0.5) + 
            (evidence.volume * 0.3) + 
            (evidence.volatility * 0.2)
        ) / 100.0
        
        consistency_factor = evidence.consistency / 100.0
        execution_factor = evidence.execution / 100.0
        
        # 2. Probability Logic
        # Using geometric mean prevents a terrible setup from being rescued by execution
        # but prevents "Good" setups from dropping to a coin flip.
        base_probability = math.sqrt(directional_quality * opportunity_quality)
        
        # Consistency modulates the final probability.
        probability = base_probability * (0.2 + (consistency_factor * 0.8))
        probability = min(1.0, max(0.0, probability))
        
        # 3. Confidence & Uncertainty Logic
        # Confidence measures how certain we are about the probability, NOT how bullish it is.
        # High consistency and high execution = high confidence in the math.
        confidence = (consistency_factor * 0.7) + (execution_factor * 0.3)
        confidence = min(1.0, max(0.0, confidence))
        
        uncertainty = max(0.0, 1.0 - confidence)
        
        # 4. Bounds Logic
        lower_bound = max(0.0, probability - (uncertainty / 2.0))
        upper_bound = min(1.0, probability + (uncertainty / 2.0))
        
        # 5. Explainability Layer
        reasons = []
        warnings = []
        
        if evidence.trend >= 70:
            reasons.append("+ Trend alignment significantly boosts probability")
        elif evidence.trend <= 30:
            warnings.append("- Unaligned trend collapses probability")
            
        if evidence.momentum >= 70:
            reasons.append("+ Above-average momentum supports expected move")
            
        if evidence.execution >= 70:
            reasons.append("+ High execution quality secures edge")
        elif evidence.execution <= 30:
            warnings.append("- Poor execution quality severely penalizes viability")
            
        if evidence.consistency >= 70:
            reasons.append("+ Robust consistency increases confidence")
        elif evidence.consistency <= 30:
            warnings.append("- Contradictory evidence destroys statistical confidence")
            
        if uncertainty > 0.40:
            warnings.append("- High uncertainty widens probability bounds")
            
        return ProbabilityResult(
            probability=probability,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            uncertainty=uncertainty,
            confidence=confidence,
            reasons=reasons,
            warnings=warnings
        )