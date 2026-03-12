from aiogram.fsm.state import State, StatesGroup


class ChatWithAlex(StatesGroup):
    """FSM states for chat with Alex"""

    active = State()
