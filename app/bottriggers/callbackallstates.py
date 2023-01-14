from app.bot import dispatcher, bot_object

from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from app.data.keyspace import *
from app.data.states import StateMachine

from app.core.dbhelper import *
from app.core import keybords as kb
from app.core.datetimehelper import *
from app.core.callbackparser import parseForData
from app.core.parsers.scheduleparsercashmanager import ScheduleParserCashManager

from app.bottriggers.corefunctions import process_schedule_dates,\
    process_schedule_teacher_dates, process_schedule_place_dates


# Поиск расписания для группы
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.GROUP == parseForData(c.data, 0), state='*')
async def process_callback_schedule_group(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    group_name = parseForData(call_data, index=0, sep=Separators.DATA_META)
    await update_last_group_for_user(callback_query.from_user.id, int(code), group_name)
    date = startDayOfWeek(datetime.date.today())

    await process_schedule_dates(callback_query, state, date)

    user_data = await get_all_from_user(callback_query.from_user.id)
    saved_groups = await get_saved_groups(callback_query.from_user.id)
    is_can_save = await can_save_group(callback_query.from_user.id)
    is_in_saved = (user_data[DatabaseColumnsUser.LAST_GROUP], user_data[DatabaseColumnsUser.LAST_GROUP_NAME]) in saved_groups
    if is_in_saved:
        keyboard = InlineKeyboardMarkup(row_width=1)
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, user_data[DatabaseColumnsUser.LAST_GROUP],
                                              user_data[DatabaseColumnsUser.LAST_GROUP_NAME],
                                              IdCommandKeyWords.REMOVE_GROUP, text="Удалить группу")

        await bot_object.send_message(callback_query.from_user.id, "Удалить группу из сохраненных?", reply_markup=keyboard)

    elif is_can_save:
        keyboard = InlineKeyboardMarkup(row_width=1)
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, user_data[DatabaseColumnsUser.LAST_GROUP],
                                              user_data[DatabaseColumnsUser.LAST_GROUP_NAME],
                                              IdCommandKeyWords.SAVE_GROUP, text="Сохранить группу")

        await bot_object.send_message(callback_query.from_user.id, "Добавить группу в сохраненные?",
                                      reply_markup=keyboard)

    else:
        await bot_object.send_message(callback_query.from_user.id, "Максимальное количество сохраненных групп!")
    await bot_object.answer_callback_query(callback_query.id)
    await StateMachine.LESSON_STATE.set()


# Сохранение группы
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.SAVE_GROUP == parseForData(c.data, 0), state='*')
async def process_callback_save_group(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    group_name = parseForData(call_data, index=0, sep=Separators.DATA_META)
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f"Группа {group_name} сохранена!")
    await save_group_for_user(callback_query.from_user.id, code, group_name)


# Удаление группы
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.REMOVE_GROUP == parseForData(c.data, 0), state='*')
async def process_callback_save_group(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    group_name = parseForData(call_data, index=0, sep=Separators.DATA_META)
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f"Группа {group_name} удалена!")
    await remove_group_for_user(callback_query.from_user.id, code, group_name)


# Поиск расписания для преподавателя
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.TEACHER == parseForData(c.data, 0), state='*')
async def process_callback_schedule_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    teacher_name = await ScheduleParserCashManager.getTeacherNameByID(code)
    await update_last_teacher_for_user(callback_query.from_user.id, int(code), teacher_name)
    date = startDayOfWeek(datetime.date.today())
    await process_schedule_teacher_dates(callback_query, state, date)

    data = await get_all_from_user(callback_query.from_user.id)

    saved_teachers = await get_saved_teachers(callback_query.from_user.id)
    is_can_save = await can_save_teacher(callback_query.from_user.id)
    is_in_saved = (data[DatabaseColumnsUser.LAST_TEACHER], data[DatabaseColumnsUser.LAST_TEACHER_NAME]) in saved_teachers
    if is_in_saved:
        keyboard = InlineKeyboardMarkup(row_width=1)
        kb.ModifyKeyboard.addCacheTeacherButton(keyboard, data[DatabaseColumnsUser.LAST_TEACHER],
                                                data[DatabaseColumnsUser.LAST_TEACHER_NAME],
                                                IdCommandKeyWords.REMOVE_TEACHER, text="Удалить преподавателя")

        await bot_object.send_message(callback_query.from_user.id, "Удалить преподавателя из сохраненных?", reply_markup=keyboard)

    elif is_can_save:
        keyboard = InlineKeyboardMarkup(row_width=1)
        kb.ModifyKeyboard.addCacheTeacherButton(keyboard, data[DatabaseColumnsUser.LAST_TEACHER],
                                                data[DatabaseColumnsUser.LAST_TEACHER_NAME],
                                                IdCommandKeyWords.SAVE_TEACHER, text="Сохранить преподавателя")

        await bot_object.send_message(callback_query.from_user.id, "Добавить преподавателя в сохраненные?",
                                      reply_markup=keyboard)

    else:
        await bot_object.send_message(callback_query.from_user.id, "Максимальное количество сохраненных преподавателей!")

    await bot_object.answer_callback_query(callback_query.id)
    await StateMachine.TEACHER_LESSON_STATE.set()


# Сохранение преподавателя
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.SAVE_TEACHER == parseForData(c.data, 0), state='*')
async def process_callback_save_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    teacher_name = await ScheduleParserCashManager.getTeacherNameByID(code)
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f"Преподаватель {teacher_name} сохранен!")
    await save_teacher_for_user(callback_query.from_user.id, code, teacher_name)


# Удаление преподавателя
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.REMOVE_TEACHER == parseForData(c.data, 0), state='*')
async def process_callback_save_teacher(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    teacher_name = await ScheduleParserCashManager.getTeacherNameByID(code)
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f"Преподаватель {teacher_name} удален!")
    await remove_teacher_for_user(callback_query.from_user.id, code, teacher_name)


# Поиск расписания для аудитории
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.PLACE == parseForData(c.data, 0), state='*')
async def process_callback_schedule_place(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    code_aud = parseForData(call_data, sep=Separators.DATA_META)
    code_building = parseForData(call_data, index=0, sep=Separators.DATA_META)
    await save_int_for_user(callback_query.from_user.id, DatabaseColumnsUser.CODE_AUD, code_aud)
    await save_int_for_user(callback_query.from_user.id, DatabaseColumnsUser.CODE_BUILDING, code_building)
    date = startDayOfWeek(datetime.date.today())
    await process_schedule_place_dates(callback_query, state, date)
    await bot_object.answer_callback_query(callback_query.id)
    await StateMachine.PLACE_LESSON_STATE.set()

