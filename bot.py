import logging

from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from data import config
import data.emojizedb as edb
from data.messages import *
from data.keyspace import *
from data.commands import COMMANDS
from data.states import StateMachine

from core import keybords as kb
from core.datetimehelper import *

logging.basicConfig(level=logging.INFO)

bot_object = Bot(token=config.TOKEN)
dispatcher = Dispatcher(bot_object, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())


# Команды вкладки меню
@dispatcher.message_handler(commands=[COMMANDS.START], state='*')
async def process_start_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = kb.InitialKeyboard.getKeyboard()

    if StateKeyWords.SAVED_GROUP in data:
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[StateKeyWords.SAVED_GROUP],
                                              data[StateKeyWords.SAVED_GROUP_NAME],
                                              IdCommandKeyWords.GROUP, text="Сохраненная группа:")
    if StateKeyWords.GROUP in data and data[StateKeyWords.GROUP] != data.get(StateKeyWords.SAVED_GROUP):
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[StateKeyWords.GROUP],
                                              data[StateKeyWords.GROUP_NAME],
                                              IdCommandKeyWords.GROUP, text="Расписание для группы")

    kb.ModifyKeyboard.addPolyLinkGroupButton(keyboard)
    em = edb.FULL_MOON_WITH_FACE if isDayTime(datetime.datetime.now().time()) else edb.NEW_MOON_WITH_FACE
    await message.answer(emojize(em) + " Добро пожаловать!", reply_markup=keyboard)

    # Используется, чтобы сбросить предыдущее состояние (не важно какое оно было)
    await StateMachine.MAIN_STATE.set()




