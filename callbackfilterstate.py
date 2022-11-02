from bot import dispatcher, bot_object

from core import keybords as kb
from aiogram import types
from data.messages import *
from data.keyspace import *
from aiogram.dispatcher import FSMContext
from core.callbackparser import parseForData
from data.states import StateMachine

from core.parsers.scheduleparsercashmanager import ScheduleParserCashManager

from corefunctions import process_answer_institute, process_answer_ed_form
import data.emojizedb as edb

# Обработка кнопок с поиском расписания по фильтрам


# Выбор формы обучения после института
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.INSTITUTE in c.data, state=StateMachine.FILTER_GROUP)
async def process_callback_institutes(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    await state.update_data(institute=code)
    await bot_object.answer_callback_query(callback_query.id)
    name = await ScheduleParserCashManager.getInstituteNameByID(code)
    await bot_object.send_message(callback_query.from_user.id, f'Вы выбрали "{name}" ')
    await process_answer_ed_form(callback_query, state)


# Выбор степени обучения после формы обучения
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.ED_FORM in c.data, state=StateMachine.FILTER_GROUP)
async def process_callback_education_form(callback_query: types.CallbackQuery, state: FSMContext):
    code = parseForData(callback_query.data)
    keyboard = kb.ScheduleKeyboard.createKeyboardRows(EDUCATION_DEGREE_RU, IdCommandKeyWords.ED_DEGREE)
    await state.update_data(ed_form=code)
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f'Вы выбрали форму "{EDUCATION_FORMS_RU[code]}" \n'
                                  + emojize(edb.LAST_QUARTER_MOON) + 'Ступень образования?',
                                  reply_markup=keyboard)


# Выбор курса после выбора степени образования
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.ED_DEGREE in c.data, state=StateMachine.FILTER_GROUP)
async def process_callback_education_degree(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    await state.update_data(ed_degree=code)
    data = await state.get_data()
    await bot_object.answer_callback_query(callback_query.id)

    if StateKeyWords.INSTITUTE not in data \
            or StateKeyWords.ED_FORM not in data:
        await bot_object.send_message(callback_query.from_user.id, f'{emojize(edb.CRY)} Нет необходимых параметров, начните '
                                                            f'сначала!')
        await process_answer_institute(callback_query, state)
        return

    levels = await ScheduleParserCashManager.getCourses(data[StateKeyWords.INSTITUTE],
                                                        data[StateKeyWords.ED_FORM],
                                                        data[StateKeyWords.ED_DEGREE])

    if len(levels) == 0:
        await bot_object.send_message(callback_query.from_user.id, f'{emojize(edb.CRY)} Здесь нет групп, выберите другие '
                                                            f'параметры!')
        await process_answer_ed_form(callback_query, state)
        return
    await bot_object.send_message(callback_query.from_user.id, f'Вы выбрали степень "{EDUCATION_DEGREE_RU[code]}"')
    keyboard = kb.ScheduleKeyboard.createKeyboardListRows(levels, IdCommandKeyWords.LEVEL)
    await bot_object.send_message(callback_query.from_user.id, emojize(edb.WANING_CRESCENT_MOON) + 'Курс?',
                                  reply_markup=keyboard)


# Поиск групп после выбора курса
@dispatcher.callback_query_handler(lambda c: IdCommandKeyWords.LEVEL in c.data, state=StateMachine.FILTER_GROUP)
async def process_callback_level(callback_query: types.CallbackQuery, state: FSMContext):
    code = int(parseForData(callback_query.data))
    await state.update_data(level=code)
    data = await state.get_data()
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f'Вы выбрали {code} курс')

    if StateKeyWords.INSTITUTE not in data \
            or StateKeyWords.ED_FORM not in data \
            or StateKeyWords.ED_DEGREE not in data:
        await bot_object.send_message(callback_query.from_user.id, f'{emojize(edb.CRY)} Нет необходимых параметров, начните '
                                                            f'сначала!')
        await process_answer_institute(callback_query, state)
        return

    groups = await ScheduleParserCashManager.getGroupsByParameters(data[StateKeyWords.INSTITUTE],
                                                                   data[StateKeyWords.ED_FORM],
                                                                   data[StateKeyWords.ED_DEGREE],
                                                                   data[StateKeyWords.LEVEL])

    if len(groups) == 0:
        await bot_object.send_message(callback_query.from_user.id, f'{emojize(edb.CRY)} Здесь нет групп, выберите другие '
                                                            f'параметры!')
        await process_answer_ed_form(callback_query, state)
        return

    keyboard = kb.ScheduleKeyboard.createKeyboardRows(groups, IdCommandKeyWords.GROUP, rows_count=2)
    await bot_object.send_message(callback_query.from_user.id, emojize(edb.NEW_MOON) + 'Группа?', reply_markup=keyboard)
