"""
==========================================================
QuantEdge AI
Risk Result Contract
==========================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass(slots=True, frozen=True)
class RiskResult:
    expected_loss: float
    downside_multiple: float
    stop_quality: float
    capital_at_risk: float

    reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def summary(self) -> str:
        lines = [
            f"Expected Loss:     {self.expected_loss:.4f}",
            f"Downside Multiple: {self.downside_multiple:.4f}",
            f"Stop Quality:      {self.stop_quality:.4f}",
            f"Capital at Risk:   {self.capital_at_risk:.4f}"
        ]
        return "\n".join(lines)
