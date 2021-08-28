from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from messages import *

stateZeroBtn = InlineKeyboardButton('Состояние 0', callback_data=STATE_0.NAME_STATE)
stateOneBtn = InlineKeyboardButton('Состояние 1', callback_data=STATE_1.NAME_STATE)
stateStdBtn = InlineKeyboardButton('Перезагрузка', callback_data=STD_STATE.NAME_STATE)

stateMarkup = InlineKeyboardMarkup(row_width=2).row(stateZeroBtn, stateOneBtn).add(stateStdBtn)
