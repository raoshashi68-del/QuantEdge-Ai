"""
==========================================================
QuantEdge AI
Expected Return Engine
==========================================================
"""

from models.evidence_vector import EvidenceVector
from models.expected_return_result import ExpectedReturnResult

class ExpectedReturnEngine:
    def __init__(self):
        pass

    def build(self, evidence: EvidenceVector) -> ExpectedReturnResult:
        structure_score = evidence.structure / 100.0
        volatility_score = evidence.volatility / 100.0
        momentum_score = evidence.momentum / 100.0
        execution_score = evidence.execution / 100.0
        
        # 1. Expected Return Base (Weighted Feasibility)
        # Weights: Structure 40%, Volatility 25%, Momentum 20%, Execution 15%
        expected_return = (
            (structure_score * 0.40) +
            (volatility_score * 0.25) +
            (momentum_score * 0.20) +
            (execution_score * 0.15)
        )
        
        # 2. Reward and Risk Multiples
        # Target multiple mathematically expands based on return feasibility. Max 3.0x.
        target_multiple = expected_return * 3.0
        
        # Downside multiple is inversely proportional to structural safety and execution slippage.
        # Strong structure and execution mean tight stops and minimal slippage.
        structural_safety = (structure_score * 0.70) + (execution_score * 0.30)
        downside_multiple = max(0.1, 1.0 - structural_safety)
        
        # 3. Reward/Risk Ratio
        reward_risk = target_multiple / downside_multiple
        
        # 4. Explainability Layer
        reasons = []
        warnings = []
        
        if evidence.structure >= 70:
            reasons.append("+ Target highly feasible due to clear structural path (e.g. ORB breakout)")
        elif evidence.structure <= 30:
            warnings.append("- Target blocked by nearby resistance/structure")
            
        if evidence.volatility >= 70:
            reasons.append("+ Sufficient ATR expansion supports reaching target")
        elif evidence.volatility <= 30:
            warnings.append("- Tiny ATR makes target mathematically improbable")
            
        if evidence.momentum >= 70:
            reasons.append("+ Strong momentum acceleration supports sustained move")
            
        if evidence.execution >= 70:
            reasons.append("+ Tight spreads maximize achievable real return")
        elif evidence.execution <= 30:
            warnings.append("- Wide spreads and high friction heavily reduce real return")
            
        return ExpectedReturnResult(
            expected_return=expected_return,
            target_multiple=target_multiple,
            downside_multiple=downside_multiple,
            reward_risk=reward_risk,
            reasons=reasons,
            warnings=warnings
        )
