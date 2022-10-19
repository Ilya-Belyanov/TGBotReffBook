import logging
import datetime

from aiogram.utils.emoji import emojize
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext

import data.emojizedb as edb
from data.messages import *
from data.keyspace import *
from data.commands import COMMANDS

from core import keybords as kb
from core.datetimehelper import *
from core.callbackparser import parseForData
from core.answercreator import beautifySchedule
from core.parsers.scheduleparser import ScheduleParser
from data import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())


# Команды вкладки меню
@dispatcher.message_handler(commands=[COMMANDS.START], state='*')
async def process_start_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = kb.InitialKeyboard.createKeyboard()
    if StateKeyWords.GROUP in data:
        kb.InitialKeyboard.addCacheGroupButton(keyboard, data[StateKeyWords.GROUP],
                                               data[StateKeyWords.GROUP_NAME],
                                               IdCommandKeyWords.GROUP)
    em = edb.FULL_MOON_WITH_FACE if isDayTime(datetime.datetime.now().time()) else edb.NEW_MOON_WITH_FACE
    await message.answer(emojize(em) + " Добро пожаловать!", reply_markup=keyboard)


@dispatcher.message_handler(commands=[COMMANDS.HELP], state='*')
async def process_help_command(message: types.Message):
    await message.reply(md.text(COMMANDS_MESS), parse_mode=types.ParseMode.MARKDOWN)


# Работа с обработкой кнопок
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.getScheduleTxt, state='*')
async def process_callback_state_std(callback_query: types.CallbackQuery):
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(ScheduleParser.getInstitutes(), IdCommandKeyWords.INSTITUTE)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, emojize(edb.FULL_MOON) + ' Институт?', reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.INSTITUTE in c.data, state='*')
async def process_callback_institutes(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(EDUCATION_FORMS_RU, IdCommandKeyWords.ED_FORM)
    await state.update_data(institute=code)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, emojize(edb.WANING_GIBBOUS_MOON) + ' Форма обучения?',
                           reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.ED_FORM in c.data, state='*')
async def process_callback_education_form(callback_query: types.CallbackQuery, state: FSMContext):
    code = parseForData(callback_query.data)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(EDUCATION_DEGREE_RU, IdCommandKeyWords.ED_DEGREE)
    await state.update_data(ed_form=code)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, emojize(edb.LAST_QUARTER_MOON) + 'Ступень образования?',
                           reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.ED_DEGREE in c.data, state='*')
async def process_callback_education_degree(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    await state.update_data(ed_degree=code)
    data = await state.get_data()
    keyboard = kb.ScheduleKeyboard.createKeyboardListRows(ScheduleParser.getCourses(data[StateKeyWords.INSTITUTE],
                                                                                    data[StateKeyWords.ED_FORM],
                                                                                    data[StateKeyWords.ED_DEGREE]),
                                                          IdCommandKeyWords.LEVEL)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, emojize(edb.WANING_CRESCENT_MOON) + 'Курс?',
                           reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.LEVEL in c.data, state='*')
async def process_callback_level(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    await state.update_data(level=code)
    data = await state.get_data()
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(
        ScheduleParser.getGroupsByParameters(data[StateKeyWords.INSTITUTE],
                                             data[StateKeyWords.ED_FORM],
                                             data[StateKeyWords.ED_DEGREE],
                                             data[StateKeyWords.LEVEL]),
        IdCommandKeyWords.GROUP, rows_count=2)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, emojize(edb.NEW_MOON) + 'Группа?', reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.GROUP in c.data, state='*')
async def process_callback_group(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    group_name = parseForData(call_data, index=0, sep=Separators.DATA_META)
    await state.update_data(group=code)
    await state.update_data(group_name=group_name)
    date = startDayOfWeek(datetime.date.today())
    await process_schedule_dates(callback_query, state, date)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES in c.data, state='*')
async def process_callback_dates(callback_query: types.CallbackQuery, state: FSMContext):
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    await process_schedule_dates(callback_query, state, date)


async def process_schedule_dates(callback_query: types.CallbackQuery, state: FSMContext, date: datetime.date):
    data = await state.get_data()
    await state.update_data(current_date=date)
    lessons = ScheduleParser.getLessons(data[StateKeyWords.INSTITUTE], data[StateKeyWords.GROUP], date)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(createPrevNextWeeks(date), IdCommandKeyWords.DATES, 3)
    await bot.answer_callback_query(callback_query.id)
    answers = beautifySchedule(lessons, date)
    for answer in answers:
        await bot.send_message(callback_query.from_user.id, answer, parse_mode=types.ParseMode.MARKDOWN_V2)
    await bot.send_message(callback_query.from_user.id, emojize(edb.CALENDAR) + "Выбрать другую неделю",
                           reply_markup=keyboard)


# Неизвестная команда
@dispatcher.message_handler(content_types=types.ContentType.ANY, state='*')
async def unknown_message(msg: types.Message):
    await msg.reply(UNKNOWN_MESS, parse_mode=types.ParseMode.MARKDOWN)
