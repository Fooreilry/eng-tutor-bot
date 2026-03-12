from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    """FSM states for user onboarding flow"""

    # user info
    name = State()
    level = State()
    interests = State()
    additional = State()


class PlacementTest(StatesGroup):
    """FSM states for placement test flow"""

    in_progress = State()


class ChatWithAlex(StatesGroup):
    """FSM states for chat with Alex"""

    active = State()
