"""
==========================================================
QuantEdge AI
Expected Return Result Contract
==========================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass(slots=True, frozen=True)
class ExpectedReturnResult:
    expected_return: float
    target_multiple: float
    downside_multiple: float
    reward_risk: float

    reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def summary(self) -> str:
        lines = [
            f"Expected Return:   {self.expected_return:.4f}",
            f"Target Multiple:   {self.target_multiple:.4f}",
            f"Downside Multiple: {self.downside_multiple:.4f}",
            f"Reward/Risk:       {self.reward_risk:.4f}"
        ]
        return "\n".join(lines)
