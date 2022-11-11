from aiogram import types
import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from bot import dispatcher

from core import keybords as kb
from core.parsers.scheduleparsercashmanager import ScheduleParserCashManager

from data.keyspace import *
import data.emojizedb as edb
from data.commands import COMMANDS
from data.messages import COMMANDS_MESS

from bottriggers.corefunctions import process_start_menu


# Вызов главного меню
@dispatcher.message_handler(commands=[COMMANDS.START], state='*')
async def process_start_command(message: types.Message, state: FSMContext):
    await process_start_menu(message.from_user.id, state)


# Ответ на запрос /help
@dispatcher.message_handler(commands=[COMMANDS.HELP], state='*')
async def process_help_command(message: types.Message):
    await message.reply(COMMANDS_MESS, parse_mode=types.ParseMode.MARKDOWN)


# Ответ на запрос /parameters
@dispatcher.message_handler(commands=[COMMANDS.PARAMETERS], state='*')
async def process_param_command(message: types.Message, state: FSMContext):
    answer = md.bold("Последний раз вы ввели следующие параметры") + ":"
    data = await state.get_data()
    answer += "\n"
    name = emojize(edb.NO_ENTRY_SIGN)
    if StateKeyWords.INSTITUTE in data:
        name = await ScheduleParserCashManager.getInstituteNameByID(data[StateKeyWords.INSTITUTE])
    answer += md.bold("Институт") + " - " + name
    answer += "\n"
    answer += md.bold("Форма") + " - " + (EDUCATION_FORMS_RU[data[StateKeyWords.ED_FORM]]
                                          if StateKeyWords.ED_FORM in data else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    answer += md.bold("Степень") + " - " + (EDUCATION_DEGREE_RU[data[StateKeyWords.ED_DEGREE]]
                                            if StateKeyWords.ED_DEGREE in data else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    answer += md.bold("Курс") + " - " + (
        str(data[StateKeyWords.LEVEL]) if StateKeyWords.LEVEL in data else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    answer += md.bold("Группа") + " - " + (
        data[StateKeyWords.GROUP_NAME] if StateKeyWords.GROUP_NAME in data else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    answer += md.bold("Сохраненная Группа") + " - " + (
        data[StateKeyWords.SAVED_GROUP_NAME] if StateKeyWords.SAVED_GROUP_NAME in data else emojize(edb.NO_ENTRY_SIGN))
    await message.reply(md.text(answer), parse_mode=types.ParseMode.MARKDOWN)


# Ответ на запрос /saved
@dispatcher.message_handler(commands=[COMMANDS.SAVED], state='*')
async def process_help_saved(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = InlineKeyboardMarkup(row_width=1)
    is_smth = False
    if StateKeyWords.SAVED_GROUP in data:
        is_smth = True
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[StateKeyWords.SAVED_GROUP],
                                              data[StateKeyWords.SAVED_GROUP_NAME],
                                              IdCommandKeyWords.GROUP, text="Группа:")

    if StateKeyWords.SAVED_TEACHER in data:
        is_smth = True
        kb.ModifyKeyboard.addCacheTeacherButton(keyboard, data[StateKeyWords.SAVED_TEACHER],
                                                data[StateKeyWords.SAVED_TEACHER_NAME],
                                                IdCommandKeyWords.TEACHER, text="Преподаватель:")

    if StateKeyWords.GROUP in data and data[StateKeyWords.GROUP] != data.get(StateKeyWords.SAVED_GROUP):
        is_smth = True
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[StateKeyWords.GROUP],
                                              data[StateKeyWords.GROUP_NAME],
                                              IdCommandKeyWords.GROUP, text="Последняя группа:")

    if StateKeyWords.TEACHER in data and data[StateKeyWords.TEACHER] != data.get(StateKeyWords.SAVED_TEACHER):
        is_smth = True
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[StateKeyWords.TEACHER],
                                              data[StateKeyWords.TEACHER_NAME],
                                              IdCommandKeyWords.TEACHER, text="Последний пр-ль:")

    if is_smth:
        await message.answer("Сохраненные и последние поиски!", reply_markup=keyboard)
    else:
        await message.answer("Никаких сохранений нет!")
