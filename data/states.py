from aiogram.dispatcher.filters.state import State, StatesGroup


class StateMachine(StatesGroup):
    MAIN_STATE = State()
    GROUP_NAME = State()
