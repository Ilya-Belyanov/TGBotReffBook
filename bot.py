import logging
import datetime

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext

import config
from data import *
from datetimehelper import *
import keybords as kb
from scheduleparser import ScheduleParser

from messages import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())


# Команды вкладки меню
@dispatcher.message_handler(commands=[COMMANDS.START], state='*')
async def process_start_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = kb.InitialKeyboard.createKeyboard()
    if "group" in data:
        kb.InitialKeyboard.addCacheGroupButton(keyboard, data["group"], data["group_name"], IdCommandKeyWords.GROUP)
    await message.answer("Добро пожаловать!", reply_markup=keyboard)


@dispatcher.message_handler(commands=[COMMANDS.HELP], state='*')
async def process_help_command(message: types.Message):
    await message.reply(md.text(COMMANDS_MESS), parse_mode=types.ParseMode.MARKDOWN)


# Работа с обработкой кнопок
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.getScheduleTxt, state='*')
async def process_callback_state_std(callback_query: types.CallbackQuery):
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(ScheduleParser.getInstitutes(), IdCommandKeyWords.INSTITUTE)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Институт?', reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.INSTITUTE in c.data, state='*')
async def process_callback_institutes(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(EDUCATION_FORMS_RU, IdCommandKeyWords.ED_FORM)
    await state.update_data(institute=code)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Форма обучения?', reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.ED_FORM in c.data, state='*')
async def process_callback_education_form(callback_query: types.CallbackQuery, state: FSMContext):
    code = parseForData(callback_query.data)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(EDUCATION_DEGREE_RU, IdCommandKeyWords.ED_DEGREE)
    await state.update_data(ed_form=code)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Ступень образования?',
                           reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.ED_DEGREE in c.data, state='*')
async def process_callback_education_degree(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    await state.update_data(ed_degree=code)
    data = await state.get_data()
    keyboard = kb.ScheduleKeyboard.createKeyboardListRows(ScheduleParser.getCourses(data['institute'],
                                                                                    data['ed_form'],
                                                                                    data['ed_degree']),
                                                          IdCommandKeyWords.LEVEL)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Курс?', reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.LEVEL in c.data, state='*')
async def process_callback_level(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    await state.update_data(level=code)
    data = await state.get_data()
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(ScheduleParser.getGroupsByParameters(data['institute'],
                                                                                           data['ed_form'],
                                                                                           data['ed_degree'],
                                                                                           data['level']),
                                                      IdCommandKeyWords.GROUP, rows_count=2)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Группа?', reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.GROUP in c.data, state='*')
async def process_callback_group(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    call_list_data = call_data.split("|")
    code = int(call_list_data[1])
    await state.update_data(group=code)
    await state.update_data(group_name=call_list_data[0])
    data = await state.get_data()
    date = startDayOfWeek(datetime.date.today())
    lessons = ScheduleParser.getLessons(data['institute'], data['group'], date)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(formeThreeWeekRange(date), IdCommandKeyWords.DATES, 3)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, md.text(beautifySchedule(lessons, date)),
                           reply_markup=keyboard, parse_mode=types.ParseMode.MARKDOWN)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES in c.data, state='*')
async def process_callback_dates(callback_query: types.CallbackQuery, state: FSMContext):
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    data = await state.get_data()
    await state.update_data(current_date=date)
    lessons = ScheduleParser.getLessons(data['institute'], data['group'], date)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(formeThreeWeekRange(date), IdCommandKeyWords.DATES, 3)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, md.text(beautifySchedule(lessons, date)),
                           reply_markup=keyboard, parse_mode=types.ParseMode.MARKDOWN)
