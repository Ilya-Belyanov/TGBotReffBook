import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dispatcher, bot_object

from core.callbackparser import parseForData

from data.keyspace import IdCommandKeyWords
from data.states import StateMachine

from bottriggers.corefunctions import process_schedule_dates, process_schedule_teacher_dates, process_schedule_place_dates


# Поиск расписания на другую неделю для группы - обработка кнопки
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES in c.data, state=StateMachine.LESSON_STATE)
async def process_callback_lesson_on_dates_group(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    await process_schedule_dates(callback_query, state, date)


# Поиск расписания на другую неделю для преподавателя - обработка кнопки
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES in c.data, state=StateMachine.TEACHER_LESSON_STATE)
async def process_callback_lesson_on_dates_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    await process_schedule_teacher_dates(callback_query, state, date)


# Поиск расписания на другую неделю для аудитории - обработка кнопки
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES in c.data, state=StateMachine.PLACE_LESSON_STATE)
async def process_callback_lesson_on_dates_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    await process_schedule_place_dates(callback_query, state, date)
