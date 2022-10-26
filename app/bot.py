import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

<<<<<<< HEAD
import config

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w')
=======
logging.basicConfig(level=logging.INFO)
>>>>>>> 44754cd... Create Docker build

try:
    token = open('/run/secrets/token', 'r').readline()
    bot_object = Bot(token=token)
except IOError:
    exit(-1)

dispatcher = Dispatcher(bot_object, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())





