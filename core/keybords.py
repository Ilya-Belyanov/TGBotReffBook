from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.keyspace import Separators


class InitialKeyboard:
    getScheduleTxt = 'schedule'

    @staticmethod
    def createKeyboard():
        getScheduleBtn = InlineKeyboardButton('Все расписания', callback_data=InitialKeyboard.getScheduleTxt)
        return InlineKeyboardMarkup(row_width=1).row(getScheduleBtn)

    @staticmethod
    def addCacheGroupButton(markup: InlineKeyboardMarkup, group_id: int, group_name: str, key_word: str):
        getCachedScheduleBtn = InlineKeyboardButton(f'Расписание для группы {group_name}',
                                                    callback_data=key_word + Separators.KEY_DATA
                                                    + group_name + Separators.DATA_META + str(group_id))
        markup.add(getCachedScheduleBtn)


class ScheduleKeyboard:
    @staticmethod
    def createKeyboardRows(rows: dict, key_word: str, rows_count: int = 1):
        rows_markup = InlineKeyboardMarkup(row_width=rows_count)
        for row_key in rows.keys():
            btn = InlineKeyboardButton(rows[row_key], callback_data=key_word + Separators.KEY_DATA + str(row_key))
            rows_markup.insert(btn)
        return rows_markup

    @staticmethod
    def createKeyboardListRows(rows: list, key_word: str):
        rows_markup = InlineKeyboardMarkup(row_width=1)
        for row in rows:
            btn = InlineKeyboardButton(row, callback_data=key_word + Separators.KEY_DATA + str(row))
            rows_markup.add(btn)
        return rows_markup