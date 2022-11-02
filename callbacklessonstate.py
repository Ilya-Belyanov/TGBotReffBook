import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dispatcher

from core.callbackparser import parseForData

from data.keyspace import IdCommandKeyWords
from data.states import StateMachine

from corefunctions import process_schedule_dates


# Поиск расписания на другую даты - обработка кнопки
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES in c.data, state=StateMachine.LESSON_STATE)
async def process_callback_dates(callback_query: types.CallbackQuery, state: FSMContext):
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    await process_schedule_dates(callback_query, state, date)
