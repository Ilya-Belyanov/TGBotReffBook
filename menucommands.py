from bot import dispatcher
from data.commands import COMMANDS
from data.messages import *
import data.emojizedb as edb
from core.parsers.scheduleparsercashmanager import ScheduleParserCashManager
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.keyspace import *


@dispatcher.message_handler(commands=[COMMANDS.HELP], state='*')
async def process_help_command(message: types.Message, state: FSMContext):
    await message.reply(COMMANDS_MESS, parse_mode=types.ParseMode.MARKDOWN)


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