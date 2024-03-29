from app.bot import bot_object

from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import FSMContext

from app.core.dbhelper import *
from app.core import keybords as kb
from app.core.datetimehelper import *
from app.core.answercreator import beautifySchedule
from app.core.parsers.scheduleparsercashmanager import ScheduleParserCashManager

from app.data.keyspace import *
import app.data.emojizedb as edb
from app.data.states import StateMachine


# Многоразовые функции с вопросами


# Вызов стартового меню
async def process_start_menu(id: int, state: FSMContext):
    keyboard = kb.InitialKeyboard.getKeyboard()
    kb.ModifyKeyboard.addPolyLinkGroupButton(keyboard)
    em = edb.FULL_MOON_WITH_FACE if isDayTime(datetime.datetime.now().time()) else edb.NEW_MOON_WITH_FACE
    await bot_object.send_message(id, emojize(em) + " Добро пожаловать!", reply_markup=keyboard)
    # Используется, чтобы сбросить предыдущее состояние (неважно какое оно было)
    await StateMachine.MAIN_STATE.set()


# Поиск институтов
async def process_answer_institute(callback_query: types.CallbackQuery, state: FSMContext):
    inst = await ScheduleParserCashManager.getInstitutes()
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(inst, IdCommandKeyWords.INSTITUTE)
    await bot_object.send_message(callback_query.message.chat.id, emojize(edb.FULL_MOON) + ' Институт?',
                                  reply_markup=keyboard)


# Поиск формы обучения
async def process_answer_ed_form(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(EDUCATION_FORMS_RU, IdCommandKeyWords.ED_FORM)
    await bot_object.send_message(callback_query.message.chat.id, emojize(edb.WANING_GIBBOUS_MOON) + ' Форма обучения?',
                                  reply_markup=keyboard)


# Поиск расписания по дате и группе в state
async def process_schedule_dates(callback_query: types.CallbackQuery, state: FSMContext, date: datetime.date):
    await process_schedule_dates_id(callback_query.message.chat.id, state, date)


async def process_schedule_dates_from_msg(msg: types.Message, state: FSMContext, date: datetime.date):
    await process_schedule_dates_id(msg.chat.id, state, date)


async def process_schedule_dates_id(id, state: FSMContext, date: datetime.date):
    last_group = await get_from_user(id, DatabaseColumnsUser.LAST_GROUP)
    await state.update_data(current_date=date)
    lessons = await ScheduleParserCashManager.getLessons(last_group, date)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(createPrevNextWeeks(date), IdCommandKeyWords.DATES, 3)
    answers = beautifySchedule(lessons, date)
    for answer in answers:
        await bot_object.send_message(id, answer, parse_mode=types.ParseMode.MARKDOWN_V2)
    await bot_object.send_message(id, emojize(edb.CALENDAR) + "Выбрать другую неделю",
                                  reply_markup=keyboard)
    await bot_object.send_message(id, "Ввести дату недели: ")


# Поиск расписания по дате и по учителю в state
async def process_schedule_teacher_dates(callback_query, state: FSMContext, date: datetime.date):
    await process_schedule_teacher_dates_id(callback_query.message.chat.id, state, date)


async def process_schedule_teacher_dates_from_msg(msg: types.Message, state: FSMContext, date: datetime.date):
    await process_schedule_teacher_dates_id(msg.chat.id, state, date)


async def process_schedule_teacher_dates_id(id, state: FSMContext, date: datetime.date):
    last_teacher = await get_from_user(id, DatabaseColumnsUser.LAST_TEACHER)
    await state.update_data(current_date=date)
    lessons = await ScheduleParserCashManager.getTeacherLessons(last_teacher, date)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(createPrevNextWeeks(date), IdCommandKeyWords.DATES, 3)
    answers = beautifySchedule(lessons, date)
    for answer in answers:
        await bot_object.send_message(id, answer, parse_mode=types.ParseMode.MARKDOWN_V2)
    await bot_object.send_message(id, emojize(edb.CALENDAR) + "Выбрать другую неделю",
                                  reply_markup=keyboard)
    await bot_object.send_message(id, "Ввести дату недели: ")


# Поиск расписания по дате и по аудитории в state
async def process_schedule_place_dates(callback_query: types.CallbackQuery, state: FSMContext, date: datetime.date):
    await process_schedule_place_dates_id(callback_query.message.chat.id, state, date)


async def process_schedule_place_dates_from_msg(msg: types.Message, state: FSMContext, date: datetime.date):
    await process_schedule_place_dates_id(msg.chat.id, state, date)


async def process_schedule_place_dates_id(id, state: FSMContext, date: datetime.date):
    data = await get_all_from_user(id)
    await state.update_data(current_date=date)
    lessons = await ScheduleParserCashManager.getPlaceLessons(data[DatabaseColumnsUser.CODE_BUILDING],
                                                              data[DatabaseColumnsUser.CODE_AUD],
                                                              date)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(createPrevNextWeeks(date), IdCommandKeyWords.DATES, 3)
    answers = beautifySchedule(lessons, date)
    for answer in answers:
        await bot_object.send_message(id, answer, parse_mode=types.ParseMode.MARKDOWN_V2)
    await bot_object.send_message(id, emojize(edb.CALENDAR) + "Выбрать другую неделю",
                                  reply_markup=keyboard)
    await bot_object.send_message(id, "Ввести дату недели: ")
