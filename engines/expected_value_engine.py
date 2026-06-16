"""
==========================================================
QuantEdge AI
Expected Value Engine
==========================================================
"""

from models.probability_result import ProbabilityResult
from models.expected_return_result import ExpectedReturnResult
from models.risk_result import RiskResult
from models.expected_value_result import ExpectedValueResult

class ExpectedValueEngine:
    def __init__(self):
        pass

    def build(self, prob: ProbabilityResult, ret: ExpectedReturnResult, risk: RiskResult) -> ExpectedValueResult:
        
        # 1. Component calculations
        upside_component = prob.probability * ret.expected_return
        
        # (1 - P(win)) represents the probability of hitting the stop/failure
        downside_component = (1.0 - prob.probability) * risk.expected_loss
        
        # 2. Expected Value
        expected_value = upside_component - downside_component
        
        # 3. Edge calculation
        total_range = upside_component + downside_component
        edge = (upside_component / total_range) if total_range > 0 else 0.0
        
        # 4. Explainability Layer
        reasons = []
        warnings = []
        
        if expected_value > 0:
            reasons.append("+ Mathematical expectation is strictly positive")
            if upside_component > (downside_component * 2):
                reasons.append("+ Upside component heavily outweighs downside exposure")
        elif expected_value < 0:
            warnings.append("- Mathematical expectation is strictly negative (guaranteed bleed)")
            
        if prob.probability == 0.0:
            warnings.append("- Zero probability of success zeroes out entire expected return")
            
        if prob.probability == 1.0:
            reasons.append("+ Absolute certainty of success ignores stop loss risk entirely")
            
        return ExpectedValueResult(
            expected_value=expected_value,
            upside_component=upside_component,
            downside_component=downside_component,
            edge=edge,
            reasons=reasons,
            warnings=warnings
        )
