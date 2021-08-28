import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import config
import keybords as kb

from messages import *
from states import MachStates

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())


@dispatcher.message_handler(commands=[COMMANDS.START[1:]])
async def process_start_command(message: types.Message):
    await message.answer(STD_STATE.START)


@dispatcher.message_handler(commands=[COMMANDS.START[1:]], state=MachStates.STATE_0)
async def process_start_command(message: types.Message):
    await message.answer(STATE_0.START)


@dispatcher.message_handler(commands=[COMMANDS.START[1:]], state=MachStates.STATE_1)
async def process_start_command(message: types.Message):
    await message.answer(STATE_1.START)


@dispatcher.message_handler(commands=[COMMANDS.HELP[1:]])
async def process_help_command(message: types.Message):
    message_text = md.text(STD_STATE.HELP, COMMANDS_MESS, sep='\n')
    await bot.send_message(message.from_user.id, message_text,
                           parse_mode=types.ParseMode.MARKDOWN)


@dispatcher.message_handler(commands=[COMMANDS.HELP[1:]], state=MachStates.STATE_1 | MachStates.STATE_0)
async def process_help_command(message: types.Message):
    message_text = md.text(STATE_0.HELP, COMMANDS_MESS, sep='\n')
    await bot.send_message(message.from_user.id, message_text,
                           parse_mode=types.ParseMode.MARKDOWN)


@dispatcher.message_handler(commands=[COMMANDS.CHANGE_STATE[1:]], state='*')
async def process_setstate_command(message: types.Message):
    await message.answer("Выберите состояние", reply_markup=kb.stateMarkup)


@dispatcher.callback_query_handler(lambda c: c.data == STD_STATE.NAME_STATE, state='*')
async def process_callback_state_std(callback_query: types.CallbackQuery):
    state = dispatcher.current_state(user=callback_query.from_user.id)
    await state.reset_state()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Перезагрузка состояния')


@dispatcher.callback_query_handler(lambda c: c.data == STATE_0.NAME_STATE, state='*')
async def process_callback_state_0(callback_query: types.CallbackQuery):
    state = dispatcher.current_state(user=callback_query.from_user.id)
    await state.set_state(MachStates.all()[0])
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Установлено состояние 0')


@dispatcher.callback_query_handler(lambda c: c.data == STATE_1.NAME_STATE, state='*')
async def process_callback_state_1(callback_query: types.CallbackQuery):
    state = dispatcher.current_state(user=callback_query.from_user.id)
    await state.set_state(MachStates.all()[1])
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Установлено состояние 1')


@dispatcher.message_handler(state='*')
async def echo(message: types.Message):
    await message.answer(message.text)


@dispatcher.message_handler(content_types=types.ContentType.ANY, state='*')
async def unknown_message(msg: types.Message):
    await msg.reply(UNKNOWN_MESS, parse_mode=types.ParseMode.MARKDOWN)
