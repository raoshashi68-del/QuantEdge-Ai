"""
==========================================================
QuantEdge AI
Position Snapshot
==========================================================
"""

class Position:
    def __init__(self, trade_id, timestamp, candidate, decision_reason):
        # Entry Identity (Immutable Snapshot)
        self.trade_id = trade_id
        self.entry_time = timestamp
        self.symbol = candidate.symbol
        self.option_symbol = getattr(candidate, 'option_symbol', '')
        self.direction = candidate.direction
        self.strike = candidate.strike
        self.expiry = getattr(candidate, 'expiry', '')
        self.entry_price = candidate.option_price
        self.quantity = 1  # Default logic
        self.status = "OPEN"
        
        # Inference Objects Snapshot
        self.evidence = candidate.evidence
        self.probability_result = candidate.probability_result
        self.expected_return_result = candidate.expected_return_result
        self.risk_result = candidate.risk_result
        self.expected_value_result = candidate.expected_value_result
        self.confidence_result = candidate.confidence_result
        self.final_score = getattr(candidate, 'score', 0.0)
        self.decision_reason = decision_reason
        
        # Exit State
        self.exit_time = None
        self.exit_price = None
        self.exit_reason = None
        
        # Realized Metrics
        self.pnl = 0.0
        self.realized_return = 0.0
        self.prediction_error = 0.0
        self.holding_time = 0.0
        
    def close(self, exit_time, exit_price, exit_reason):
        if self.status == "REALIZED":
            return
            
        self.exit_time = exit_time
        self.exit_price = exit_price
        self.exit_reason = exit_reason
        self.status = "REALIZED"
        
        # Calculate Realized Metrics
        # Assuming Long Option structure (buy to open, sell to close)
        self.pnl = (self.exit_price - self.entry_price) * self.quantity
        
        if self.entry_price > 0:
            self.realized_return = (self.exit_price - self.entry_price) / self.entry_price
        else:
            self.realized_return = 0.0
            
        expected_ret = self.expected_return_result.expected_return if self.expected_return_result else 0.0
        self.prediction_error = self.realized_return - expected_ret
        
        # Holding time in minutes
        delta = self.exit_time - self.entry_time
        self.holding_time = delta.total_seconds() / 60.0
