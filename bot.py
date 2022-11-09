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
    keyboard = kb.InitialKeyboard.getKeyboard()
    kb.ModifyKeyboard.addPolyLinkGroupButton(keyboard)
    em = edb.FULL_MOON_WITH_FACE if isDayTime(datetime.datetime.now().time()) else edb.NEW_MOON_WITH_FACE
    await message.answer(emojize(em) + " Добро пожаловать!", reply_markup=keyboard)

    # Используется, чтобы сбросить предыдущее состояние (неважно какое оно было)
    await StateMachine.MAIN_STATE.set()




