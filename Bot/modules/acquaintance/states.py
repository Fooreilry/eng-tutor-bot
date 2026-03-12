from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    """FSM states for user onboarding flow"""

    name = State()
    level = State()
    interests = State()
    additional = State()
