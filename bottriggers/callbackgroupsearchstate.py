from aiogram import types

from aiogram.dispatcher import FSMContext
from bot import dispatcher, bot_object

from core.parsers.scheduleparsercashmanager import ScheduleParserCashManager
from core import keybords as kb

from data.states import StateMachine
from data.commands import COMMANDS
from data.keyspace import *


# Обработка введенного текста
@dispatcher.message_handler(content_types=types.ContentType.TEXT, state=StateMachine.GROUP_NAME)
async def process_callback_search_groups(msg: types.Message):
    txt = msg.text
    groups = await ScheduleParserCashManager.getGroupsByText(txt)
    if len(groups) == 0:
        await bot_object.send_message(msg.from_user.id, f"Группы не найдены. Напишите еще раз (или выберите команду /{COMMANDS.START}):")
        return
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(groups, IdCommandKeyWords.GROUP, rows_count=2)
    await bot_object.send_message(msg.from_user.id, "Найденные группы", reply_markup=keyboard)
    await bot_object.send_message(msg.from_user.id, f"Не нашли? Напишите еще раз (для выхода введите /{COMMANDS.START}):")
