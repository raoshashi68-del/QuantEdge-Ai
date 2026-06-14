"""
==========================================================

QuantEdge AI

Position Manager

Responsibilities
----------------
1. Open Position
2. Update Live Price
3. Update Trailing Stop
4. Partial Exit
5. Full Exit
6. Track Statistics

==========================================================
"""

from datetime import datetime

from core.state import PositionState

from models.position import Position


class PositionManager:

    def __init__(self):

        self.positions = {}

    # --------------------------------------------------

    def open_position(

        self,

        candidate,

        quantity,

        entry_price,

        stop_loss,

        target,

    ):

        position = Position(

            symbol=candidate.symbol,

            direction=candidate.direction,

            option_symbol=candidate.option_symbol,

            quantity=quantity,

            entry_price=entry_price,

            stop_loss=stop_loss,

            target=target,

        )

        position.current_price = entry_price
        position.highest_price = entry_price
        position.lowest_price = entry_price

        self.positions[position.option_symbol] = position

        return position

    # --------------------------------------------------

    def get(

        self,

        option_symbol,

    ):

        return self.positions.get(option_symbol)

    # --------------------------------------------------

    def update_price(

        self,

        option_symbol,

        current_price,

    ):

        position = self.get(option_symbol)

        if position is None:

            return None

        position.update_price(current_price)

        return position

    # --------------------------------------------------

    def move_trailing_stop(

        self,

        option_symbol,

        new_stop,

    ):

        position = self.get(option_symbol)

        if position is None:

            return None

        if new_stop > position.trailing_stop:

            position.trailing_stop = new_stop

            position.status = PositionState.TRAILING.value

        return position

    # --------------------------------------------------

    def protect_position(

        self,

        option_symbol,

        new_stop,

    ):

        position = self.get(option_symbol)

        if position is None:

            return None

        if new_stop > position.stop_loss:

            position.stop_loss = new_stop

            position.status = PositionState.PROTECTED.value

        return position

    # --------------------------------------------------

    def partial_exit(

        self,

        option_symbol,

        exit_price,

        quantity,

    ):

        position = self.get(option_symbol)

        if position is None:

            return None

        quantity = min(quantity, position.quantity)

        realized = (

            exit_price -

            position.entry_price

        ) * quantity

        position.realized_pnl += realized

        position.quantity -= quantity

        position.status = PositionState.SCALE_OUT.value

        if position.quantity == 0:

            position.status = PositionState.CLOSED.value

            position.exit_price = exit_price

            position.exit_time = datetime.now()

        return position

    # --------------------------------------------------

    def close_position(

        self,

        option_symbol,

        exit_price,

        reason,

    ):

        position = self.get(option_symbol)

        if position is None:

            return None

        position.close(

            exit_price,

            reason,

        )

        return position

    # --------------------------------------------------

    def active_positions(self):

        return [

            p

            for p in self.positions.values()

            if p.status != PositionState.CLOSED.value

        ]

    # --------------------------------------------------

    def closed_positions(self):

        return [

            p

            for p in self.positions.values()

            if p.status == PositionState.CLOSED.value

        ]