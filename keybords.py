from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from messages import *

stateZeroBtn = InlineKeyboardButton('Состояние 0', callback_data=STATE_0.NAME_STATE)
stateOneBtn = InlineKeyboardButton('Состояние 1', callback_data=STATE_1.NAME_STATE)
stateStdBtn = InlineKeyboardButton('Перезагрузка', callback_data=STD_STATE.NAME_STATE)

stateMarkup = InlineKeyboardMarkup(row_width=2).row(stateZeroBtn, stateOneBtn).add(stateStdBtn)


class InitialKeyboard:
    getScheduleTxt = 'schedule'
    getScheduleBtn = InlineKeyboardButton('Получить расписание', callback_data=getScheduleTxt)
    stateMarkup = InlineKeyboardMarkup(row_width=1).row(getScheduleBtn)


class ScheduleKeyboard:
    @staticmethod
    def createKeyboardRows(rows: dict, rows_count: int = 1):
        rows_markup = InlineKeyboardMarkup(row_width=rows_count)
        for row_key in rows.keys():
            btn = InlineKeyboardButton(rows[row_key], callback_data=str(row_key))
            rows_markup.insert(btn)
        return rows_markup

    @staticmethod
    def createKeyboardListRows(rows: list):
        rows_markup = InlineKeyboardMarkup(row_width=1)
        for row in rows:
            btn = InlineKeyboardButton(row, callback_data=str(row))
            rows_markup.add(btn)
        return rows_markup


