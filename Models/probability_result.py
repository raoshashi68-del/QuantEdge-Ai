"""
==========================================================
QuantEdge AI
Probability Result Contract
==========================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class ProbabilityResult:
    probability: float
    lower_bound: float
    upper_bound: float
    uncertainty: float
    confidence: float

    reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def summary(self) -> str:
        lines = [
            f"Probability: {self.probability:.4f}",
            f"Lower Bound: {self.lower_bound:.4f}",
            f"Upper Bound: {self.upper_bound:.4f}",
            f"Uncertainty: {self.uncertainty:.4f}",
            f"Confidence:  {self.confidence:.4f}",
        ]
        return "\n".join(lines)
