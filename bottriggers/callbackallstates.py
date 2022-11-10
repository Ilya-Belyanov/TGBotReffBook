from bot import dispatcher, bot_object

from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from data.keyspace import *
from data.states import StateMachine

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
    await state.update_data(group=code)
    await state.update_data(group_name=group_name)
    date = startDayOfWeek(datetime.date.today())

    await process_schedule_dates(callback_query, state, date)

    data = await state.get_data()

    if data[StateKeyWords.GROUP] != data.get(StateKeyWords.SAVED_GROUP):
        keyboard = InlineKeyboardMarkup(row_width=1)
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[StateKeyWords.GROUP],
                                              data[StateKeyWords.GROUP_NAME],
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
    await state.update_data(saved_group=code)
    await state.update_data(saved_group_name=group_name)
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f"Группа {group_name} сохранена!")


# Поиск расписания для преподавателя
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.TEACHER in c.data, state='*')
async def process_callback_schedule_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    teacher_name = await ScheduleParserCashManager.getTeacherNameByID(code)
    await state.update_data(teacher=code)
    await state.update_data(teacher_name=teacher_name)
    date = startDayOfWeek(datetime.date.today())
    await process_schedule_teacher_dates(callback_query, state, date)

    data = await state.get_data()

    if data[StateKeyWords.TEACHER] != data.get(StateKeyWords.SAVED_TEACHER):
        keyboard = InlineKeyboardMarkup(row_width=1)
        kb.ModifyKeyboard.addCacheTeacherButton(keyboard, data[StateKeyWords.TEACHER],
                                                data[StateKeyWords.TEACHER_NAME],
                                                IdCommandKeyWords.SAVE_TEACHER, text="Сохранить преподавателя")

        await bot_object.send_message(callback_query.from_user.id, "Вы можете сохранить преподавателя, чтобы не "
                                                                   "вводить его каждый раз", reply_markup=keyboard)

    await StateMachine.TEACHER_LESSON_STATE.set()


# Сохранение группы
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.SAVE_TEACHER in c.data, state='*')
async def process_callback_save_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    teacher_name = await ScheduleParserCashManager.getTeacherNameByID(code)
    await state.update_data(saved_teacher=code)
    await state.update_data(saved_teacher_name=teacher_name)
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f"Преподаватель {teacher_name} сохранен!")


# Поиск расписания для аудитории
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.PLACE in c.data, state='*')
async def process_callback_schedule_place(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    code_aud = parseForData(call_data, sep=Separators.DATA_META)
    code_building = parseForData(call_data, index=0, sep=Separators.DATA_META)
    await state.update_data(code_aud=code_aud)
    await state.update_data(code_building=code_building)
    date = startDayOfWeek(datetime.date.today())
    await process_schedule_place_dates(callback_query, state, date)
    await StateMachine.PLACE_LESSON_STATE.set()
