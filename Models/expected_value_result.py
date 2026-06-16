"""
==========================================================
QuantEdge AI
Expected Value Result Contract
==========================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass(slots=True, frozen=True)
class ExpectedValueResult:
    expected_value: float
    upside_component: float
    downside_component: float
    edge: float

    reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def summary(self) -> str:
        lines = [
            f"Expected Value:     {self.expected_value:.4f}",
            f"Upside Component:   {self.upside_component:.4f}",
            f"Downside Component: {self.downside_component:.4f}",
            f"Edge:               {self.edge:.4f}"
        ]
        return "\n".join(lines)
