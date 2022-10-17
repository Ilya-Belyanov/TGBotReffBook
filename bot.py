import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext

import config
from data import *
import keybords as kb
from scheduleparser import ScheduleParser

from messages import *
from states import MachStates

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())


@dispatcher.message_handler(commands=[COMMANDS.START])
async def process_start_command(message: types.Message):
    await message.answer(STD_STATE.START, reply_markup=kb.InitialKeyboard.stateMarkup)


@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.getScheduleTxt, state='*')
async def process_callback_state_std(callback_query: types.CallbackQuery):
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(ScheduleParser.getInstitutes())
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Секундочку...', reply_markup=keyboard)
    await MachStates.STATE_INSTITUTE.set()


@dispatcher.callback_query_handler(state=MachStates.STATE_INSTITUTE)
async def process_callback_institutes(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(callback_query.data)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(EDUCATION_FORMS_RU)
    await state.update_data(institute=code)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Получил код: ' + str(code), reply_markup=keyboard)
    await MachStates.STATE_ED_FORM.set()


@dispatcher.callback_query_handler(state=MachStates.STATE_ED_FORM)
async def process_callback_education_form(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(EDUCATION_DEGREE_RU)
    await state.update_data(ed_form=code)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Получил код: ' + code + " " + EDUCATION_FORMS_RU[code],
                           reply_markup=keyboard)
    await MachStates.STATE_ED_DEGREE.set()


@dispatcher.callback_query_handler(state=MachStates.STATE_ED_DEGREE)
async def process_callback_education_degree(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(callback_query.data)
    await state.update_data(ed_degree=code)
    data = await state.get_data()
    keyboard = kb.ScheduleKeyboard.createKeyboardListRows(ScheduleParser.getCourses(data['institute'],
                                                                                    data['ed_form'],
                                                                                    data['ed_degree']))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Получил код: ' + str(code) + " " + EDUCATION_DEGREE_RU[code],
                           reply_markup=keyboard)
    await MachStates.STATE_LEVEL.set()


@dispatcher.callback_query_handler(state=MachStates.STATE_LEVEL)
async def process_callback_level(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(callback_query.data)
    await state.update_data(level=code)
    data = await state.get_data()
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(ScheduleParser.getGroupsByParameters(data['institute'],
                                                                                           data['ed_form'],
                                                                                           data['ed_degree'],
                                                                                           data['level']))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           'Получил код: ' + str(code),
                           reply_markup=keyboard)
    await MachStates.STATE_GROUP.set()


@dispatcher.callback_query_handler(state=MachStates.STATE_GROUP)
async def process_callback_level(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(callback_query.data)
    await state.update_data(group=code)
    data = await state.get_data()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           'Получил код: ' + str(code))
    await MachStates.STATE_GROUP.set()

'''
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
    
'''