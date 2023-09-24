from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot import dispatcher, bot_object

from app.core.parsers.scheduleparsercashmanager import ScheduleParserCashManager
from app.core.datetimehelper import simplifyStr
from app.core import keybords as kb

from app.data.states import StateMachine
from app.data.keyspace import *


# Обработка введенного текста
@dispatcher.message_handler(content_types=types.ContentType.TEXT, state=StateMachine.PLACE_NAME)
async def process_callback_search_place(msg: types.Message, state: FSMContext):
    txt = simplifyStr(msg.text)
    places = await ScheduleParserCashManager.getPlacesByText(txt)
    menu = kb.InitialKeyboard.getToMenuKeyboard()
    if len(places) == 0:
        await bot_object.send_message(msg.chat.id, f"Аудитории не найдены. Напишите еще раз:", reply_markup=menu)
        return
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(places, IdCommandKeyWords.PLACE, rows_count=1)
    await bot_object.send_message(msg.chat.id, "Найденные аудитории", reply_markup=keyboard)
    await bot_object.send_message(msg.chat.id, f"Не нашли? Напишите еще раз:", reply_markup=menu)
