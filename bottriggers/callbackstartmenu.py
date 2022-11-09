from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dispatcher, bot_object

from core import keybords as kb

from data.messages import *
from data.states import StateMachine

from bottriggers.corefunctions import process_answer_institute

# Функции можно обрабатывать со всех состояний


# Поиск институтов и начало поиска группы по фильтру
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.getScheduleTxt, state='*')
async def process_callback_get_schedule(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.answer_callback_query(callback_query.id)
    await process_answer_institute(callback_query, state)
    await StateMachine.FILTER_GROUP.set()


# Поиск по группе
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.searchGroupTxt, state='*')
async def process_callback_search_groups_command(callback_query: types.CallbackQuery):
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f"Введите группу (для выхода /{COMMANDS.START}):")
    await StateMachine.GROUP_NAME.set()


# Поиск по группе
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.searchTeacherTxt, state='*')
async def process_callback_search_teacher_command(callback_query: types.CallbackQuery):
    await bot_object.answer_callback_query(callback_query.id)
    await bot_object.send_message(callback_query.from_user.id, f"Введите имя преподавателя "
                                                               f"(для выхода /{COMMANDS.START}):")
    await StateMachine.TEACHER_NAME.set()
