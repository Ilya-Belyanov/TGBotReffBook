from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot import dispatcher, bot_object
from app.core.dbhelper import all_users, save_int_for_user

from app.data.states import StateMachine
from app.data.keyspace import DatabaseColumnsUser


# Обработка введенного текста
@dispatcher.message_handler(content_types=types.ContentType.ANY, state=StateMachine.WRITE_TO_ALL)
async def process_callback_write_to_all(msg: types.Message, state: FSMContext):
    users = await all_users()
    for user in users:
        try:
            if msg.text is not None:
                await bot_object.send_message(user[0], msg.text)
            if msg.photo is not None and len(msg.photo) > 0:
                await bot_object.send_photo(user[0], photo=msg.photo[-1].file_id,
                                            caption=msg.caption if msg.caption else "")
            if msg.document is not None:
                await bot_object.send_document(user[0], document=msg.document.file_id,
                                               caption=msg.caption if msg.caption else "")
            await save_int_for_user(user[0], DatabaseColumnsUser.ACTIVE, 1)
        except Exception as e:
            await save_int_for_user(user[0], DatabaseColumnsUser.ACTIVE, 0)
    await StateMachine.MAIN_STATE.set()
