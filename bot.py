import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from data import config

logging.basicConfig(level=logging.INFO)

bot_object = Bot(token=config.TOKEN)
dispatcher = Dispatcher(bot_object, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())





