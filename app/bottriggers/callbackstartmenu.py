from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot import dispatcher, bot_object

from app.core import keybords as kb
from app.core.googleanalytics import analytic_wrapper_with_message

from app.data.states import StateMachine
from app.data.commands import COMMANDS

from app.bottriggers.corefunctions import process_answer_institute, process_start_menu

# Функции можно обрабатывать со всех состояний


# Поиск институтов и начало поиска группы по фильтру
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.getScheduleTxt, state='*')
@analytic_wrapper_with_message(action="Group_filter_search_btn")
async def process_callback_get_schedule(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot_object.answer_callback_query(callback_query.id)
    await process_answer_institute(callback_query, state)
    await StateMachine.FILTER_GROUP.set()


# Поиск по группе
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.searchGroupTxt, state='*')
@analytic_wrapper_with_message(action="Group_search_btn")
async def process_callback_search_groups_command(callback_query: types.CallbackQuery):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot_object.answer_callback_query(callback_query.id)
    menu = kb.InitialKeyboard.getToMenuKeyboard()
    await bot_object.send_message(callback_query.from_user.id, f"Введите группу:", reply_markup=menu)
    await StateMachine.GROUP_NAME.set()


# Поиск по преподавателю
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.searchTeacherTxt, state='*')
@analytic_wrapper_with_message(action="Teacher_search_btn")
async def process_callback_search_teacher_command(callback_query: types.CallbackQuery):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot_object.answer_callback_query(callback_query.id)
    menu = kb.InitialKeyboard.getToMenuKeyboard()
    await bot_object.send_message(callback_query.from_user.id, f"Введите имя преподавателя:", reply_markup=menu)
    await StateMachine.TEACHER_NAME.set()


# Поиск по аудитории
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.searchPlaceTxt, state='*')
@analytic_wrapper_with_message(action="Audit_search_btn")
async def process_callback_search_place_command(callback_query: types.CallbackQuery):
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot_object.answer_callback_query(callback_query.id)
    menu = kb.InitialKeyboard.getToMenuKeyboard()
    await bot_object.send_message(callback_query.from_user.id, f"Введите названии аудитории:", reply_markup=menu)
    await StateMachine.PLACE_NAME.set()


# Возвращение в меню
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.toMenuTxt, state='*')
@analytic_wrapper_with_message(action=COMMANDS.START)
async def process_callback_to_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await process_start_menu(callback_query.from_user.id, state)
    await bot_object.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
