from bot import bot_object

from aiogram.dispatcher import FSMContext
from data.keyspace import *
from core import keybords as kb
from aiogram import types
from core.datetimehelper import *
from core.answercreator import beautifySchedule
from aiogram.utils.emoji import emojize
import data.emojizedb as edb

from core.parsers.scheduleparsercashmanager import ScheduleParserCashManager


# Многоразовые функции с вопросами

# Поиск институтов
async def process_answer_institute(callback_query: types.CallbackQuery, state: FSMContext):
    inst = await ScheduleParserCashManager.getInstitutes()
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(inst, IdCommandKeyWords.INSTITUTE)
    await bot_object.send_message(callback_query.from_user.id, emojize(edb.FULL_MOON) + ' Институт?', reply_markup=keyboard)


# Поиск формы обучения
async def process_answer_ed_form(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(EDUCATION_FORMS_RU, IdCommandKeyWords.ED_FORM)
    await bot_object.send_message(callback_query.from_user.id, emojize(edb.WANING_GIBBOUS_MOON) + ' Форма обучения?',
                                  reply_markup=keyboard)


# Поиск расписания по дате и группе в state
async def process_schedule_dates(callback_query: types.CallbackQuery, state: FSMContext, date: datetime.date):
    data = await state.get_data()
    await state.update_data(current_date=date)
    lessons = await ScheduleParserCashManager.getLessons(data[StateKeyWords.GROUP], date)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(createPrevNextWeeks(date), IdCommandKeyWords.DATES, 3)
    await bot_object.answer_callback_query(callback_query.id)
    answers = beautifySchedule(lessons, date)
    for answer in answers:
        await bot_object.send_message(callback_query.from_user.id, answer, parse_mode=types.ParseMode.MARKDOWN_V2)
    await bot_object.send_message(callback_query.from_user.id, emojize(edb.CALENDAR) + "Выбрать другую неделю",
                                  reply_markup=keyboard)


# Поиск расписания по дате и по учителю в state
async def process_schedule_teacher_dates(callback_query: types.CallbackQuery, state: FSMContext, date: datetime.date):
    data = await state.get_data()
    await state.update_data(current_date=date)
    lessons = await ScheduleParserCashManager.getTeacherLessons(data[StateKeyWords.TEACHER], date)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(createPrevNextWeeks(date), IdCommandKeyWords.DATES, 3)
    await bot_object.answer_callback_query(callback_query.id)
    answers = beautifySchedule(lessons, date)
    for answer in answers:
        await bot_object.send_message(callback_query.from_user.id, answer, parse_mode=types.ParseMode.MARKDOWN_V2)
    await bot_object.send_message(callback_query.from_user.id, emojize(edb.CALENDAR) + "Выбрать другую неделю",
                                  reply_markup=keyboard)


# Поиск расписания по дате и по аудитории в state
async def process_schedule_place_dates(callback_query: types.CallbackQuery, state: FSMContext, date: datetime.date):
    data = await state.get_data()
    await state.update_data(current_date=date)
    lessons = await ScheduleParserCashManager.getPlaceLessons(data[StateKeyWords.CODE_BUILDING], data[StateKeyWords.CODE_AUD], date)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(createPrevNextWeeks(date), IdCommandKeyWords.DATES, 3)
    await bot_object.answer_callback_query(callback_query.id)
    answers = beautifySchedule(lessons, date)
    for answer in answers:
        await bot_object.send_message(callback_query.from_user.id, answer, parse_mode=types.ParseMode.MARKDOWN_V2)
    await bot_object.send_message(callback_query.from_user.id, emojize(edb.CALENDAR) + "Выбрать другую неделю",
                                  reply_markup=keyboard)
