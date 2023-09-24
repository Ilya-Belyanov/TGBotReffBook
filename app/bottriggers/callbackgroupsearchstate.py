from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot import dispatcher, bot_object

from app.core.parsers.scheduleparsercashmanager import ScheduleParserCashManager
from app.core.datetimehelper import simplifyStr
from app.core import keybords as kb

from app.data.states import StateMachine
from app.data.keyspace import *


# Обработка введенного текста
@dispatcher.message_handler(content_types=types.ContentType.TEXT, state=StateMachine.GROUP_NAME)
async def process_callback_search_groups(msg: types.Message, state: FSMContext):
    txt = simplifyStr(msg.text)
    groups = await ScheduleParserCashManager.getGroupsByText(txt)
    menu = kb.InitialKeyboard.getToMenuKeyboard()
    if len(groups) == 0:
        await bot_object.send_message(msg.chat.id, f"Группы не найдены. Напишите еще раз:", reply_markup=menu)
        return
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(groups, IdCommandKeyWords.GROUP, rows_count=2)
    await bot_object.send_message(msg.chat.id, "Найденные группы", reply_markup=keyboard)
    await bot_object.send_message(msg.chat.id, f"Не нашли? Напишите еще раз:", reply_markup=menu)
