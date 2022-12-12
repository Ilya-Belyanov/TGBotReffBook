from app.bot import dispatcher, bot_object

from aiogram import types
from aiogram.dispatcher import FSMContext

from app.data.messages import *
from app.data.states import StateMachine


# Неизвестная команда
@dispatcher.message_handler(content_types=types.ContentType.ANY, state='*')
async def unknown_message(msg: types.Message):
    await msg.reply(UNKNOWN_MESS, parse_mode=types.ParseMode.MARKDOWN)


# Нажата другая кнопка, вне этого состояния
@dispatcher.callback_query_handler(state='*')
async def process_callback_unknown_lessons(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == StateMachine.MAIN_STATE.state or current_state is None:
        await bot_object.send_message(callback_query.from_user.id, f'Вы находитесь в главном состоянии '
                                                                   f' выберите опцию по команде /{COMMANDS.START}')
    elif current_state == StateMachine.FILTER_GROUP.state:
        await bot_object.send_message(callback_query.from_user.id,
                                      f'Вы находитесь в состоянии поиска группы по фильтру,'
                                      f' для выхода введите /{COMMANDS.START}')

    elif current_state == StateMachine.GROUP_NAME.state:
        await bot_object.send_message(callback_query.from_user.id, f'Вы находитесь в состоянии поиска группы по имени'
                                                                   f' для выхода введите /{COMMANDS.START}')

    elif current_state == StateMachine.LESSON_STATE.state:
        await bot_object.send_message(callback_query.from_user.id, f'Вы находитесь в состоянии просмотра расписания,'
                                                                   f' для выхода введите /{COMMANDS.START}')
    await bot_object.answer_callback_query(callback_query.id)
