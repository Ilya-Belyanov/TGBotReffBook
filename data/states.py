from aiogram.dispatcher.filters.state import State, StatesGroup


class StateMachine(StatesGroup):
    # Основное состояние, при котором можно войти в другие
    MAIN_STATE = State()

    # Состояние поиска группы по фильтрам
    FILTER_GROUP = State()

    # Состояние поиска группы по имени
    GROUP_NAME = State()

    # Состояние поиска преподавателя по имени
    TEACHER_NAME = State()

    # Состояние поиска аудитории по имени
    PLACE_NAME = State()

    # Состояние просмотра расписания группы
    LESSON_STATE = State()

    # Состояние просмотра расписания преподавателя
    TEACHER_LESSON_STATE = State()

    # Состояние просмотра расписания аудитории
    PLACE_LESSON_STATE = State()
