from bot import dispatcher, bot_object

from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from data.keyspace import *
from data.states import StateMachine

from core.dbhelper import *
from core import keybords as kb
from core.datetimehelper import *
from core.callbackparser import parseForData
from core.parsers.scheduleparsercashmanager import ScheduleParserCashManager

from bottriggers.corefunctions import process_schedule_dates, process_schedule_teacher_dates, process_schedule_place_dates


# Поиск расписания для группы
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.GROUP in c.data, state='*')
async def process_callback_schedule_group(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    group_name = parseForData(call_data, index=0, sep=Separators.DATA_META)
    await update_last_group_for_user(callback_query.from_user.id, int(code), group_name)
    date = startDayOfWeek(datetime.date.today())

    await process_schedule_dates(callback_query, state, date)

    data = await get_all_from_user(callback_query.from_user.id)

    if data[DatabaseColumnsUser.LAST_GROUP] != data.get(DatabaseColumnsUser.SAVED_GROUP):
        keyboard = InlineKeyboardMarkup(row_width=1)
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[DatabaseColumnsUser.LAST_GROUP],
                                              data[DatabaseColumnsUser.LAST_GROUP_NAME],
                                              IdCommandKeyWords.SAVE_GROUP, text="Сохранить группу")

        await bot_object.send_message(callback_query.from_user.id, "Вы можете сохранить группу, чтобы не "
                                                                   "вводить ее каждый раз", reply_markup=keyboard)

    await StateMachine.LESSON_STATE.set()


# Сохранение группы
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.SAVE_GROUP in c.data, state='*')
async def process_callback_save_group(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    group_name = parseForData(call_data, index=0, sep=Separators.DATA_META)
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f"Группа {group_name} сохранена!")
    await save_group_for_user(callback_query.from_user.id, code, group_name)


# Поиск расписания для преподавателя
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.TEACHER in c.data, state='*')
async def process_callback_schedule_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    teacher_name = await ScheduleParserCashManager.getTeacherNameByID(code)
    await update_last_teacher_for_user(callback_query.from_user.id, int(code), teacher_name)
    date = startDayOfWeek(datetime.date.today())
    await process_schedule_teacher_dates(callback_query, state, date)

    data = await get_all_from_user(callback_query.from_user.id)

    if data[DatabaseColumnsUser.LAST_TEACHER] != data.get(DatabaseColumnsUser.SAVED_TEACHER):
        keyboard = InlineKeyboardMarkup(row_width=1)
        kb.ModifyKeyboard.addCacheTeacherButton(keyboard, data[DatabaseColumnsUser.LAST_TEACHER],
                                                data[DatabaseColumnsUser.LAST_TEACHER_NAME],
                                                IdCommandKeyWords.SAVE_TEACHER, text="Сохранить преподавателя")

        await bot_object.send_message(callback_query.from_user.id, "Вы можете сохранить преподавателя, чтобы не "
                                                                   "вводить его каждый раз", reply_markup=keyboard)

    await StateMachine.TEACHER_LESSON_STATE.set()


# Сохранение преподавателя
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.SAVE_TEACHER in c.data, state='*')
async def process_callback_save_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    teacher_name = await ScheduleParserCashManager.getTeacherNameByID(code)
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f"Преподаватель {teacher_name} сохранен!")
    await save_teacher_for_user(callback_query.from_user.id, code, teacher_name)


# Поиск расписания для аудитории
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.PLACE in c.data, state='*')
async def process_callback_schedule_place(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    code_aud = parseForData(call_data, sep=Separators.DATA_META)
    code_building = parseForData(call_data, index=0, sep=Separators.DATA_META)
    await save_int_for_user(callback_query.from_user.id, DatabaseColumnsUser.CODE_AUD, code_aud)
    await save_int_for_user(callback_query.from_user.id, DatabaseColumnsUser.CODE_BUILDING, code_building)
    date = startDayOfWeek(datetime.date.today())
    await process_schedule_place_dates(callback_query, state, date)
    await StateMachine.PLACE_LESSON_STATE.set()

