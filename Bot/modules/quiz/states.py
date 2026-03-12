from aiogram.fsm.state import State, StatesGroup


class PlacementTest(StatesGroup):
    """FSM states for placement test flow"""

    in_progress = State()
