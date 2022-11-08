from bot import dispatcher, bot_object
from aiogram import types
import itertools
from data.states import StateMachine

from core.parsers.scheduleparsercashmanager import ScheduleParserCashManager
from aiogram.dispatcher import FSMContext
from data.commands import COMMANDS
from data.keyspace import *
from core import keybords as kb


# Обработка введенного имени преподавателя
@dispatcher.message_handler(content_types=types.ContentType.TEXT, state=StateMachine.TEACHER_NAME)
async def process_callback_search_teacher(msg: types.Message, state: FSMContext):
    txt = msg.text
    groups = await ScheduleParserCashManager.getTeacherByText(txt)
    if len(groups) == 0:
        await bot_object.send_message(msg.from_user.id, f"Преподаватели не найдены. Напишите еще раз "
                                                        f"(выход /{COMMANDS.START}):")
        return

    count = (len(groups) // 10) + 1
    for i in range(count):
        item = dict(itertools.islice(groups.items(), i * 10, (i + 1) * 10))
        keyboard = kb.ScheduleKeyboard.createKeyboardRows(item, IdCommandKeyWords.TEACHER, rows_count=1)
        await bot_object.send_message(msg.from_user.id, f"Найденные преподаватели {i + 1}/{count}",
                                      reply_markup=keyboard)
    await bot_object.send_message(msg.from_user.id, f"Не нашли? Напишите еще раз (для выхода"
                                                    f" /{COMMANDS.START}):")
