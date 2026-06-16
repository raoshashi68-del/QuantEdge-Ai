"""
==========================================================
QuantEdge AI
Confidence Engine
==========================================================
"""

import math
from models.evidence_vector import EvidenceVector
from models.probability_result import ProbabilityResult
from models.expected_return_result import ExpectedReturnResult
from models.risk_result import RiskResult
from models.expected_value_result import ExpectedValueResult
from models.confidence_result import ConfidenceResult

class ConfidenceEngine:
    def __init__(self):
        pass

    def build(
        self,
        evidence: EvidenceVector,
        prob: ProbabilityResult,
        ret: ExpectedReturnResult,
        risk: RiskResult
    ) -> ConfidenceResult:
        
        # 1. Stability (35%)
        # Stability of the underlying feature foundation
        stability = evidence.consistency / 100.0
        
        # 2. Agreement (35%)
        # Do the engines agree on the trade's quality?
        prob_score = prob.probability
        return_score = min(1.0, ret.expected_return)
        risk_score = max(0.0, 1.0 - risk.expected_loss) # Invert risk so 1.0 is "Good"
        
        scores = [prob_score, return_score, risk_score]
        mean_score = sum(scores) / len(scores)
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        std_dev = math.sqrt(variance)
        
        # Max standard deviation of 0 to 1 scale is 0.5.
        agreement = max(0.0, 1.0 - (std_dev * 2.0))
        
        # 3. Uncertainty Penalty (30%)
        # Directly derived from probability uncertainty bounds
        uncertainty_penalty = prob.uncertainty
        
        # 4. Decision Clarity
        # Measures distance from the 'indecision zone' (probability = 0.5)
        # Highly bullish (0.9) and highly bearish (0.1) both yield high clarity.
        decision_clarity = min(1.0, 2.0 * abs(prob.probability - 0.5))
        
        # 5. Confidence Calculation
        # Multiply the base components by Decision Clarity to penalize coin-flips
        base_confidence = (
            (stability * 0.35) +
            (agreement * 0.35) +
            ((1.0 - uncertainty_penalty) * 0.30)
        )
        # We blend decision clarity so a pure coin flip doesn't drop confidence to absolute zero
        # but pulls it down significantly (e.g., 50% penalty).
        confidence = base_confidence * (0.5 + 0.5 * decision_clarity)
        
        # Explainability
        reasons = []
        warnings = []
        
        if agreement > 0.75:
            reasons.append("+ Independent engines are highly aligned in their assessment")
        elif agreement < 0.40:
            warnings.append("- Severe disagreement between Probability, Risk, and Return engines")
            
        if stability > 0.75:
            reasons.append("+ Underlying evidence vector is highly stable")
        elif stability < 0.40:
            warnings.append("- Underlying evidence is fragmented and unstable")
            
        if uncertainty_penalty > 0.50:
            warnings.append("- High mathematical uncertainty severely penalizes trust")
            
        return ConfidenceResult(
            confidence=confidence,
            stability=stability,
            agreement=agreement,
            uncertainty_penalty=uncertainty_penalty,
            reasons=reasons,
            warnings=warnings
        )
