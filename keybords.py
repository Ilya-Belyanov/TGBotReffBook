from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
            print(rows[row_key], str(row_key))
        return rows_markup

    @staticmethod
    def createKeyboardListRows(rows: list):
        rows_markup = InlineKeyboardMarkup(row_width=1)
        for row in rows:
            btn = InlineKeyboardButton(row, callback_data=str(row))
            rows_markup.add(btn)
        return rows_markup


