"""
==========================================================
QuantEdge AI
Risk Engine
==========================================================
"""

from models.evidence_vector import EvidenceVector
from models.risk_result import RiskResult

class RiskEngine:
    def __init__(self):
        pass

    def build(self, evidence: EvidenceVector) -> RiskResult:
        # 1. Component Risks
        # Poor structure means wide, arbitrary stops
        structural_risk = (100.0 - evidence.structure) / 100.0
        
        # High ATR requires a wider stop distance mathematically
        volatility_risk = evidence.volatility / 100.0
        
        # Poor execution translates directly to slippage on the exit order
        execution_risk = (100.0 - evidence.execution) / 100.0
        
        # Weak momentum increases the probability of hitting the stop before trailing it
        momentum_risk = (100.0 - evidence.momentum) / 100.0
        
        # 2. Expected Loss Calculation
        # Weights: Structure 40%, Volatility 30%, Execution 20%, Momentum 10%
        expected_loss = (
            (structural_risk * 0.40) +
            (volatility_risk * 0.30) +
            (execution_risk * 0.20) +
            (momentum_risk * 0.10)
        )
        
        # 3. Downside Multiple
        downside_multiple = expected_loss * 2.0
        
        # 4. Stop Quality
        # Stop quality is heavily dependent on having a clear structural invalidation point
        stop_quality = max(0.0, 1.0 - structural_risk)
        
        # 5. Capital at Risk
        # Nominal sizing assumption: scales linearly with expected downside logic
        capital_at_risk = expected_loss * 0.02
        
        # 6. Explainability Layer
        reasons = []
        warnings = []
        
        if structural_risk <= 0.30:
            reasons.append("+ Clear structural invalidation point provides tight, logical stop")
        elif structural_risk >= 0.70:
            warnings.append("- Poor structure forces arbitrary, wide stops")
            
        if volatility_risk >= 0.70:
            warnings.append("- High volatility requires widening stop, increasing expected loss")
        elif volatility_risk <= 0.30:
            reasons.append("+ Controlled volatility allows for tighter risk parameters")
            
        if execution_risk >= 0.70:
            warnings.append("- Wide spreads and low liquidity dramatically increase slippage loss")
        elif execution_risk <= 0.30:
            reasons.append("+ Excellent execution environment minimizes slippage on stop out")
            
        if momentum_risk >= 0.70:
            warnings.append("- Weak momentum increases chance of early stop out before target")
            
        return RiskResult(
            expected_loss=expected_loss,
            downside_multiple=downside_multiple,
            stop_quality=stop_quality,
            capital_at_risk=capital_at_risk,
            reasons=reasons,
            warnings=warnings
        )
