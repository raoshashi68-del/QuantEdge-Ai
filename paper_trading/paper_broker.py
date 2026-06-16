"""
==========================================================
QuantEdge AI
Paper Broker
==========================================================
"""
from datetime import datetime
from interfaces.broker import Broker
from paper_trading.position import Position
from paper_trading.trade_ledger import TradeLedger

class PaperBroker(Broker):
    def __init__(self, market_data_provider, initial_capital=100000):
        self.market_data_provider = market_data_provider
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.ledger = TradeLedger()
        self.order_number = 1

    # ------------------------------------------------
    # Market Data Delegation
    # ------------------------------------------------

    def history(self, symbol, resolution, start, end):
        return self.market_data_provider.history(symbol, resolution, start, end)

    def quote(self, symbol):
        return self.market_data_provider.quote(symbol)

    def option_chain(self, symbol):
        return self.market_data_provider.option_chain(symbol)

    # ------------------------------------------------
    # Lifecycle & Exit Logic
    # ------------------------------------------------

    def execute_decision(self, decision, current_time=None):
        if not decision or getattr(decision, 'action', '') != "EXECUTE":
            return False
            
        candidate = getattr(decision, 'candidate', None)
        if not candidate:
            return False
            
        timestamp = current_time or datetime.now()
        trade_id = f"PAPER-{self.order_number}"
        self.order_number += 1
        
        position = Position(
            trade_id=trade_id,
            timestamp=timestamp,
            candidate=candidate,
            decision_reason=getattr(decision, 'reason', '')
        )
        
        cost = position.entry_price * position.quantity
        if cost > self.cash:
            return False
            
        self.cash -= cost
        self.ledger.append(position)
        return True

    def mark_to_market(self, quotes_dict):
        """Update unrealized PnL based on current market quotes if needed.
        Currently delegated entirely to evaluate_exits.
        """
        pass

    def evaluate_exits(self, current_time, quotes_dict, is_data_end=False):
        open_positions = self.ledger.filter(status="OPEN")
        for pos in open_positions:
            current_price = quotes_dict.get(pos.option_symbol)
            if current_price is None:
                continue
                
            exit_reason = None
            
            if is_data_end:
                exit_reason = "DATA_END"
            elif current_time.hour >= 15 and current_time.minute >= 15:
                exit_reason = "END_OF_DAY"
            else:
                # Static Stop Loss / Take Profit
                exp_ret = pos.expected_return_result.expected_return if pos.expected_return_result else 0.5
                exp_loss = pos.risk_result.expected_loss if pos.risk_result else 0.2
                
                target_price = pos.entry_price * (1 + exp_ret)
                stop_price = pos.entry_price * (1 - exp_loss)
                
                if current_price >= target_price:
                    exit_reason = "TAKE_PROFIT"
                elif current_price <= stop_price:
                    exit_reason = "STOP_LOSS"
                    
            if exit_reason:
                pos.close(exit_time=current_time, exit_price=current_price, exit_reason=exit_reason)
                proceeds = pos.exit_price * pos.quantity
                self.cash += proceeds

    # ------------------------------------------------
    # Legacy Interface Compliance
    # ------------------------------------------------
    
    def place_order(self, **kwargs):
        return {"success": False, "message": "Deprecated in P1.3, use execute_decision"}

    def positions(self):
        return {p.option_symbol: p for p in self.ledger.filter(status="OPEN")}

    def orders(self):
        return self.ledger.retrieve()

    def portfolio_value(self):
        return self.cash