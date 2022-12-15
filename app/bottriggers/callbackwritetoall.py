from aiogram import types

from app.bot import dispatcher, bot_object
from app.core.dbhelper import all_users, save_int_for_user

from app.data.states import StateMachine
from app.data.keyspace import DatabaseColumnsUser


# Обработка введенного текста
@dispatcher.message_handler(content_types=types.ContentType.TEXT, state=StateMachine.WRITE_TO_ALL)
async def process_callback_write_to_all(msg: types.Message):
    txt = msg.text
    users = await all_users()
    for user in users:
        try:
            await bot_object.send_message(user[0], txt)
            await save_int_for_user(user[0], DatabaseColumnsUser.ACTIVE, 1)
        except Exception as e:
            await save_int_for_user(user[0], DatabaseColumnsUser.ACTIVE, 0)
    await StateMachine.MAIN_STATE.set()

