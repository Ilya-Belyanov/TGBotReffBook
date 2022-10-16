from aiogram.dispatcher.filters.state import State, StatesGroup


class MachStates(StatesGroup):
    STATE_INSTITUTE = State()
    STATE_ED_FORM = State()
    STATE_COURSE = State()
