from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot import dispatcher, bot_object
from app.bottriggers.corefunctions import process_schedule_dates_from_msg,\
    process_schedule_teacher_dates_from_msg, process_schedule_place_dates_from_msg

from app.core.datetimehelper import strToDate, simplifyStr, startDayOfWeek
from app.data.states import StateMachine


# Обработка введенного текста при просмоте расписания группы
@dispatcher.message_handler(content_types=types.ContentType.TEXT, state=StateMachine.LESSON_STATE)
async def process_callback_lesson_on_date(msg: types.Message, state: FSMContext):
    date, success = strToDate(simplifyStr(msg.text))
    if not success:
        return await bot_object.send_message(msg.chat.id, "Неверный формат даты!")
    await process_schedule_dates_from_msg(msg, state, date=startDayOfWeek(date))


# Обработка введенного текста при просмоте расписания учителя
@dispatcher.message_handler(content_types=types.ContentType.TEXT, state=StateMachine.TEACHER_LESSON_STATE)
async def process_callback_teacher_lesson_on_date(msg: types.Message, state: FSMContext):
    date, success = strToDate(simplifyStr(msg.text))
    if not success:
        return await bot_object.send_message(msg.chat.id, "Неверный формат даты!")
    await process_schedule_teacher_dates_from_msg(msg, state, date=startDayOfWeek(date))


# Обработка введенного текста при просмоте расписания помещения
@dispatcher.message_handler(content_types=types.ContentType.TEXT, state=StateMachine.PLACE_LESSON_STATE)
async def process_callback_teacher_lesson_on_date(msg: types.Message, state: FSMContext):
    date, success = strToDate(simplifyStr(msg.text))
    if not success:
        return await bot_object.send_message(msg.chat.id, "Неверный формат даты!")
    await process_schedule_place_dates_from_msg(msg, state, date=startDayOfWeek(date))

