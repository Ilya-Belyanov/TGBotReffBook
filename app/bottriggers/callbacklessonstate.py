import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot import dispatcher, bot_object

from app.core.callbackparser import parseForData

from app.data.keyspace import IdCommandKeyWords
from app.data.states import StateMachine

from app.bottriggers.corefunctions import process_schedule_dates,\
    process_schedule_teacher_dates, process_schedule_place_dates


# Поиск расписания на другую неделю для группы - обработка кнопки
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES == parseForData(c.data, 0), state=StateMachine.LESSON_STATE)
async def process_callback_lesson_on_dates_group(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    await process_schedule_dates(callback_query, state, date)
    await bot_object.answer_callback_query(callback_query.id)


# Поиск расписания на другую неделю для преподавателя - обработка кнопки
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES == parseForData(c.data, 0), state=StateMachine.TEACHER_LESSON_STATE)
async def process_callback_lesson_on_dates_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    await process_schedule_teacher_dates(callback_query, state, date)
    await bot_object.answer_callback_query(callback_query.id)


# Поиск расписания на другую неделю для аудитории - обработка кнопки
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES == parseForData(c.data, 0), state=StateMachine.PLACE_LESSON_STATE)
async def process_callback_lesson_on_dates_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    await process_schedule_place_dates(callback_query, state, date)
    await bot_object.answer_callback_query(callback_query.id)
