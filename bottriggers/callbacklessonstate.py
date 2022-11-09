import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dispatcher

from core.callbackparser import parseForData

from data.keyspace import IdCommandKeyWords
from data.states import StateMachine

from bottriggers.corefunctions import process_schedule_dates, process_schedule_teacher_dates


# Поиск расписания на другую неделю для группы - обработка кнопки
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES in c.data, state=StateMachine.LESSON_STATE)
async def process_callback_lesson_on_dates_group(callback_query: types.CallbackQuery, state: FSMContext):
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    await process_schedule_dates(callback_query, state, date)


# Поиск расписания на другую неделю для преподавателя - обработка кнопки
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES in c.data, state=StateMachine.TEACHER_LESSON_STATE)
async def process_callback_lesson_on_dates_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    await process_schedule_teacher_dates(callback_query, state, date)
