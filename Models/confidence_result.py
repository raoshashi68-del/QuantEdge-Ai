"""
==========================================================
QuantEdge AI
Confidence Result Contract
==========================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass(slots=True, frozen=True)
class ConfidenceResult:
    confidence: float
    stability: float
    agreement: float
    uncertainty_penalty: float

    reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def summary(self) -> str:
        lines = [
            f"Confidence:          {self.confidence:.4f}",
            f"Stability:           {self.stability:.4f}",
            f"Agreement:           {self.agreement:.4f}",
            f"Uncertainty Penalty: {self.uncertainty_penalty:.4f}"
        ]
        return "\n".join(lines)
