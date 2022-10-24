import logging
import datetime

from aiogram.utils.emoji import emojize
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config
import data.emojizedb as edb
from data.messages import *
from data.keyspace import *
from data.commands import COMMANDS

from core import keybords as kb
from core.datetimehelper import *
from core.callbackparser import parseForData
from core.answercreator import beautifySchedule
from core.parsers.scheduleparsercash import ScheduleParserCash

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())


# Команды вкладки меню
@dispatcher.message_handler(commands=[COMMANDS.START], state='*')
async def process_start_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = kb.InitialKeyboard.createKeyboard()

    if StateKeyWords.SAVED_GROUP in data:
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[StateKeyWords.SAVED_GROUP],
                                              data[StateKeyWords.SAVED_GROUP_NAME],
                                              IdCommandKeyWords.GROUP, text="Сохраненная группа:")
    if StateKeyWords.GROUP in data and data[StateKeyWords.GROUP] != data.get(StateKeyWords.SAVED_GROUP):
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[StateKeyWords.GROUP],
                                              data[StateKeyWords.GROUP_NAME],
                                              IdCommandKeyWords.GROUP, text="Расписание для группы")

    kb.ModifyKeyboard.addPolyLinkGroupButton(keyboard)
    em = edb.FULL_MOON_WITH_FACE if isDayTime(datetime.datetime.now().time()) else edb.NEW_MOON_WITH_FACE
    await message.answer(emojize(em) + " Добро пожаловать!", reply_markup=keyboard)


@dispatcher.message_handler(commands=[COMMANDS.HELP], state='*')
async def process_help_command(message: types.Message):
    await message.reply(COMMANDS_MESS, parse_mode=types.ParseMode.MARKDOWN)


@dispatcher.message_handler(commands=[COMMANDS.PARAMETERS], state='*')
async def process_param_command(message: types.Message, state: FSMContext):
    answer = md.bold("Последний раз вы ввели следующие параметры") + ":"
    data = await state.get_data()
    answer += "\n"
    answer += md.bold("Институт") + " - " + (ScheduleParserCash.getInstituteNameByID(data[StateKeyWords.INSTITUTE])
                                             if StateKeyWords.INSTITUTE in data else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    answer += md.bold("Форма") + " - " + (EDUCATION_FORMS_RU[data[StateKeyWords.ED_FORM]]
                                          if StateKeyWords.ED_FORM in data else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    answer += md.bold("Степень") + " - " + (EDUCATION_DEGREE_RU[data[StateKeyWords.ED_DEGREE]]
                                            if StateKeyWords.ED_DEGREE in data else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    answer += md.bold("Курс") + " - " + (
        str(data[StateKeyWords.LEVEL]) if StateKeyWords.LEVEL in data else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    answer += md.bold("Группа") + " - " + (
        data[StateKeyWords.GROUP_NAME] if StateKeyWords.GROUP_NAME in data else emojize(edb.NO_ENTRY_SIGN))
    answer += "\n"
    answer += md.bold("Сохраненная Группа") + " - " + (
        data[StateKeyWords.SAVED_GROUP_NAME] if StateKeyWords.SAVED_GROUP_NAME in data else emojize(edb.NO_ENTRY_SIGN))
    await message.reply(md.text(answer), parse_mode=types.ParseMode.MARKDOWN)


# Работа с обработкой кнопок
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.getScheduleTxt, state='*')
async def process_callback_state_std(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await process_answer_institute(callback_query, state)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.INSTITUTE in c.data, state='*')
async def process_callback_institutes(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    await state.update_data(institute=code)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           f'Вы выбрали "{ScheduleParserCash.getInstituteNameByID(code)}" ')
    await process_answer_ed_form(callback_query, state)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.ED_FORM in c.data, state='*')
async def process_callback_education_form(callback_query: types.CallbackQuery, state: FSMContext):
    code = parseForData(callback_query.data)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(EDUCATION_DEGREE_RU, IdCommandKeyWords.ED_DEGREE)
    await state.update_data(ed_form=code)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Вы выбрали форму "{EDUCATION_FORMS_RU[code]}"')
    await bot.send_message(callback_query.from_user.id, emojize(edb.LAST_QUARTER_MOON) + 'Ступень образования?',
                           reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.ED_DEGREE in c.data, state='*')
async def process_callback_education_degree(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    await state.update_data(ed_degree=code)
    data = await state.get_data()
    await bot.answer_callback_query(callback_query.id)

    if StateKeyWords.INSTITUTE not in data \
            or StateKeyWords.ED_FORM not in data:
        await bot.send_message(callback_query.from_user.id, f'{emojize(edb.CRY)} Нет необходимых параметров, начните '
                                                            f'сначала!')
        await process_answer_institute(callback_query, state)
        return

    levels = ScheduleParserCash.getCourses(data[StateKeyWords.INSTITUTE],
                                           data[StateKeyWords.ED_FORM],
                                           data[StateKeyWords.ED_DEGREE])

    if len(levels) == 0:
        await bot.send_message(callback_query.from_user.id, f'{emojize(edb.CRY)} Здесь нет групп, выберите другие '
                                                            f'параметры!')
        await process_answer_ed_form(callback_query, state)
        return
    await bot.send_message(callback_query.from_user.id, f'Вы выбрали степень "{EDUCATION_DEGREE_RU[code]}"')
    keyboard = kb.ScheduleKeyboard.createKeyboardListRows(levels, IdCommandKeyWords.LEVEL)
    await bot.send_message(callback_query.from_user.id, emojize(edb.WANING_CRESCENT_MOON) + 'Курс?',
                           reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.LEVEL in c.data, state='*')
async def process_callback_level(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    await state.update_data(level=code)
    data = await state.get_data()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Вы выбрали {code} курс')

    if StateKeyWords.INSTITUTE not in data \
            or StateKeyWords.ED_FORM not in data \
            or StateKeyWords.ED_DEGREE not in data:
        await bot.send_message(callback_query.from_user.id, f'{emojize(edb.CRY)} Нет необходимых параметров, начните '
                                                            f'сначала!')
        await process_answer_institute(callback_query, state)
        return

    groups = ScheduleParserCash.getGroupsByParameters(data[StateKeyWords.INSTITUTE],
                                                      data[StateKeyWords.ED_FORM],
                                                      data[StateKeyWords.ED_DEGREE],
                                                      data[StateKeyWords.LEVEL])

    if len(groups) == 0:
        await bot.send_message(callback_query.from_user.id, f'{emojize(edb.CRY)} Здесь нет групп, выберите другие '
                                                            f'параметры!')
        await process_answer_ed_form(callback_query, state)
        return

    keyboard = kb.ScheduleKeyboard.createKeyboardRows(groups, IdCommandKeyWords.GROUP, rows_count=2)
    await bot.send_message(callback_query.from_user.id, emojize(edb.NEW_MOON) + 'Группа?', reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.GROUP in c.data, state='*')
async def process_callback_group(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    group_name = parseForData(call_data, index=0, sep=Separators.DATA_META)
    await state.update_data(group=code)
    await state.update_data(group_name=group_name)
    date = startDayOfWeek(datetime.date.today())
    await bot.send_message(callback_query.from_user.id, f'Вы выбрали группу {group_name}')
    await process_schedule_dates(callback_query, state, date)

    data = await state.get_data()
    if data[StateKeyWords.GROUP] != data.get(StateKeyWords.SAVED_GROUP):
        keyboard = InlineKeyboardMarkup(row_width=1)
        kb.ModifyKeyboard.addCacheGroupButton(keyboard, data[StateKeyWords.GROUP],
                                              data[StateKeyWords.GROUP_NAME],
                                              IdCommandKeyWords.SAVE_GROUP, text="Сохранить группу")

        await bot.send_message(callback_query.from_user.id, "Вы можете сохранить группу в кэш, чтобы не вводить ее "
                                                            "каждый раз", reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.SAVE_GROUP in c.data, state='*')
async def process_callback_save_group(callback_query: types.CallbackQuery, state: FSMContext):
    call_data = parseForData(callback_query.data)
    code = parseForData(call_data, sep=Separators.DATA_META)
    group_name = parseForData(call_data, index=0, sep=Separators.DATA_META)
    await state.update_data(saved_group=code)
    await state.update_data(saved_group_name=group_name)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Группа {group_name} сохранена!")


@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.DATES in c.data, state='*')
async def process_callback_dates(callback_query: types.CallbackQuery, state: FSMContext):
    date = datetime.date.fromisoformat(parseForData(callback_query.data))
    await process_schedule_dates(callback_query, state, date)


# Многоразовые функции с вопросами
async def process_answer_institute(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(ScheduleParserCash.getInstitutes(), IdCommandKeyWords.INSTITUTE)
    await bot.send_message(callback_query.from_user.id, emojize(edb.FULL_MOON) + ' Институт?', reply_markup=keyboard)


async def process_answer_ed_form(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(EDUCATION_FORMS_RU, IdCommandKeyWords.ED_FORM)
    await bot.send_message(callback_query.from_user.id, emojize(edb.WANING_GIBBOUS_MOON) + ' Форма обучения?',
                           reply_markup=keyboard)


async def process_schedule_dates(callback_query: types.CallbackQuery, state: FSMContext, date: datetime.date):
    data = await state.get_data()
    await state.update_data(current_date=date)

    if StateKeyWords.INSTITUTE not in data \
            or StateKeyWords.GROUP not in data:
        await bot.send_message(callback_query.from_user.id, f'{emojize(edb.CRY)} Нет необходимых параметров, начните '
                                                            f'сначала!')
        await process_answer_institute(callback_query, state)
        return

    lessons = ScheduleParserCash.getLessons(data[StateKeyWords.INSTITUTE], data[StateKeyWords.GROUP], date)
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
