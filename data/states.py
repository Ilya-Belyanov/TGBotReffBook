from aiogram.dispatcher.filters.state import State, StatesGroup


class StateMachine(StatesGroup):
    MAIN_STATE = State()
    GROUP_NAME = State()
    TEACHER_NAME = State()
    FILTER_GROUP = State()
    LESSON_STATE = State()
    TEACHER_LESSON_STATE = State()
