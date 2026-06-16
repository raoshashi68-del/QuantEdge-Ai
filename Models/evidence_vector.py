"""
==========================================================

QuantEdge AI

Evidence Vector Contract

==========================================================
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class EvidenceVector:
    trend: float = 0.0
    momentum: float = 0.0
    volume: float = 0.0
    volatility: float = 0.0
    structure: float = 0.0
    execution: float = 0.0
    consistency: float = 0.0

    institutional_score: float = 0.0

    reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "trend": self.trend,
            "momentum": self.momentum,
            "volume": self.volume,
            "volatility": self.volatility,
            "structure": self.structure,
            "execution": self.execution,
            "consistency": self.consistency,
            "institutional_score": self.institutional_score,
            "reasons": self.reasons,
            "warnings": self.warnings,
            "metadata": self.metadata
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EvidenceVector':
        return cls(
            trend=data.get("trend", 0.0),
            momentum=data.get("momentum", 0.0),
            volume=data.get("volume", 0.0),
            volatility=data.get("volatility", 0.0),
            structure=data.get("structure", 0.0),
            execution=data.get("execution", 0.0),
            consistency=data.get("consistency", 0.0),
            institutional_score=data.get("institutional_score", 0.0),
            reasons=data.get("reasons", []),
            warnings=data.get("warnings", []),
            metadata=data.get("metadata", {})
        )
        
    def validate(self) -> bool:
        # All scores must be strictly 0-100
        fields_to_check = [
            self.trend, self.momentum, self.volume, self.volatility, 
            self.structure, self.execution, self.consistency, self.institutional_score
        ]
        return all(0.0 <= score <= 100.0 for score in fields_to_check)
        
    def summary(self) -> str:
        lines = [
            f"Institutional Score: {self.institutional_score:.2f}",
            f"Trend:       {self.trend:.2f}",
            f"Momentum:    {self.momentum:.2f}",
            f"Volume:      {self.volume:.2f}",
            f"Volatility:  {self.volatility:.2f}",
            f"Structure:   {self.structure:.2f}",
            f"Execution:   {self.execution:.2f}",
            f"Consistency: {self.consistency:.2f}",
            f"Reasons:     {len(self.reasons)}",
            f"Warnings:    {len(self.warnings)}"
        ]
        return "\n".join(lines)
