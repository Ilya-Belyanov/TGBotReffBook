from aiogram import types
import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from bot import dispatcher

from core import keybords as kb
from core.parsers.scheduleparsercashmanager import ScheduleParserCashManager
from core.dbhelper import add_user, get_all_from_user

from data.keyspace import *
import data.emojizedb as edb
from data.commands import COMMANDS
from data.messages import COMMANDS_MESS

from bottriggers.corefunctions import process_start_menu


# Вызов главного меню
@dispatcher.message_handler(commands=[COMMANDS.START], state='*')
async def process_start_command(message: types.Message, state: FSMContext):
    await process_start_menu(message.from_user.id, state)
    await add_user(message.from_user.id)


# Ответ на запрос /help
@dispatcher.message_handler(commands=[COMMANDS.HELP], state='*')
async def process_help_command(message: types.Message):
    await message.reply(COMMANDS_MESS, parse_mode=types.ParseMode.MARKDOWN)
    await add_user(message.from_user.id)


# Ответ на запрос /parameters
@dispatcher.message_handler(commands=[COMMANDS.PARAMETERS], state='*')
async def process_param_command(message: types.Message, state: FSMContext):
    answer = md.bold("Последний раз вы ввели следующие параметры") + ":"
    data = await get_all_from_user(message.from_user.id)
    state_data = await state.get_data()
    answer += "\n"
    name = emojize(edb.NO_ENTRY_SIGN)
    if StateKeyWords.INSTITUTE in state_data:
        name = await ScheduleParserCashManager.getInstituteNameByID(state_data[StateKeyWords.INSTITUTE])
    answer += md.bold("Институт") + " - " + name
    answer += "\n"
    ed_form = state_data.get(StateKeyWords.ED_FORM)
    answer += md.bold("Форма") + " - " + (EDUCATION_FORMS_RU[ed_form]
                                          if ed_form is not None else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    ed_degree = state_data.get(StateKeyWords.ED_DEGREE)
    answer += md.bold("Степень") + " - " + (EDUCATION_DEGREE_RU[ed_degree]
                                            if ed_degree is not None else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    lvl = state_data.get(StateKeyWords.LEVEL)
    answer += md.bold("Курс") + " - " + (str(lvl) if lvl is not None else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    answer += md.bold("Группа") + " - " + (
        data[DatabaseColumnsUser.LAST_GROUP_NAME] if DatabaseColumnsUser.LAST_GROUP_NAME in data else emojize(
            edb.NO_ENTRY_SIGN))
    answer += "\n"
    saved_group = data[DatabaseColumnsUser.SAVED_GROUP_NAME]
    answer += md.bold("Сохраненная Группа") + " - " + (
        saved_group if saved_group is not None else emojize(edb.NO_ENTRY_SIGN))
    await message.reply(md.text(answer), parse_mode=types.ParseMode.MARKDOWN)
    await add_user(message.from_user.id)


# Ответ на запрос /saved
@dispatcher.message_handler(commands=[COMMANDS.SAVED], state='*')
async def process_help_saved(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=1)
    is_smth = False
    data = await get_all_from_user(message.from_user.id)
    if data[DatabaseColumnsUser.SAVED_GROUP] is not None:
        is_smth = True
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[DatabaseColumnsUser.SAVED_GROUP],
                                              data[DatabaseColumnsUser.SAVED_GROUP_NAME],
                                              IdCommandKeyWords.GROUP, text="Группа:")

    if data[DatabaseColumnsUser.SAVED_TEACHER] is not None:
        is_smth = True
        kb.ModifyKeyboard.addCacheTeacherButton(keyboard, data[DatabaseColumnsUser.SAVED_TEACHER],
                                                data[DatabaseColumnsUser.SAVED_TEACHER_NAME],
                                                IdCommandKeyWords.TEACHER, text="Преподаватель:")

    if DatabaseColumnsUser.LAST_GROUP in data \
            and data[DatabaseColumnsUser.LAST_GROUP] != data.get(DatabaseColumnsUser.SAVED_GROUP):
        is_smth = True
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[DatabaseColumnsUser.LAST_GROUP],
                                              data[DatabaseColumnsUser.LAST_GROUP_NAME],
                                              IdCommandKeyWords.GROUP, text="Последняя группа:")

    if DatabaseColumnsUser.LAST_TEACHER in data\
            and data[DatabaseColumnsUser.LAST_TEACHER] != data.get(DatabaseColumnsUser.SAVED_TEACHER):
        is_smth = True
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[DatabaseColumnsUser.LAST_TEACHER],
                                              data[DatabaseColumnsUser.LAST_TEACHER_NAME],
                                              IdCommandKeyWords.TEACHER, text="Последний пр-ль:")

    if is_smth:
        await message.answer("Сохраненные и последние поиски!", reply_markup=keyboard)
    else:
        await message.answer("Никаких сохранений нет!")
    await add_user(message.from_user.id)
