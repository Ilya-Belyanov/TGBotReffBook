from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot import dispatcher, bot_object

from app.core import keybords as kb
from app.core.dbhelper import user_count
from app.core.googleanalytics import analytic_wrapper_with_message
from app.core.parsers.scheduleparsercashmanager import ScheduleParserCashManager

from app.data.states import StateMachine

# Функции можно обрабатывать со всех состояний


# Очистка кэша поиска по сайту расписания
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.clearCache, state='*')
@analytic_wrapper_with_message(action="Clear_cache")
async def process_callback_clear_cache(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot_object.answer_callback_query(callback_query.id)
    await ScheduleParserCashManager.clearCache()


# Показываем количество пользователей в бд
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.userCountBtn, state='*')
@analytic_wrapper_with_message(action="user_count")
async def process_callback_user_count(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    users = await user_count()
    await bot_object.send_message(callback_query.message.chat.id, f"В базе количество пользователей равно {users}")
    await bot_object.answer_callback_query(callback_query.id)


# Написать сообщение всем пользователям
@dispatcher.callback_query_handler(lambda c: c.data == kb.InitialKeyboard.writeToUsers, state='*')
@analytic_wrapper_with_message(action="write_to_all")
async def process_callback_write_to_all(callback_query: types.CallbackQuery, state: FSMContext):
    await bot_object.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot_object.send_message(callback_query.message.chat.id, f"Напишите сообщение и мы его разошлем")
    await StateMachine.WRITE_TO_ALL.set()
    await bot_object.answer_callback_query(callback_query.id)
