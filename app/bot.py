import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import config

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w')

bot_object = Bot(token=config.TOKEN)
dispatcher = Dispatcher(bot_object, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())





