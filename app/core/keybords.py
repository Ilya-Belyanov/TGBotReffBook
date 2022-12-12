from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.data.keyspace import Separators
from app.data.urls import SCHEDULE_URL


class InitialKeyboard:
    getScheduleTxt = 'schedule'
    searchGroupTxt = 'search_grp'
    searchTeacherTxt = 'search_teacher'
    searchPlaceTxt = 'search_place'
    toMenuTxt = 'menu'

    @staticmethod
    def getKeyboard():
        getScheduleBtn = InlineKeyboardButton('Найти расписание', callback_data=InitialKeyboard.getScheduleTxt)
        searchGroupBtn = InlineKeyboardButton('Поиск по группе', callback_data=InitialKeyboard.searchGroupTxt)
        searchTeacherBtn = InlineKeyboardButton('Поиск по преподавателю',
                                                callback_data=InitialKeyboard.searchTeacherTxt)
        searchPlaceBtn = InlineKeyboardButton('Поиск по аудитории',
                                              callback_data=InitialKeyboard.searchPlaceTxt)
        return InlineKeyboardMarkup(row_width=1).row(getScheduleBtn).row(searchGroupBtn).row(searchTeacherBtn).row(
            searchPlaceBtn)

    @staticmethod
    def getToMenuKeyboard():
        toMenuBtn = InlineKeyboardButton('Меню', callback_data=InitialKeyboard.toMenuTxt)
        return InlineKeyboardMarkup(row_width=1).row(toMenuBtn)


class ModifyKeyboard:
    @staticmethod
    def addCacheGroupButton(markup: InlineKeyboardMarkup, main_data: int, group_name: str, key_word: str,
                            text: str = "Группа"):
        getCachedScheduleBtn = InlineKeyboardButton(text + f' {group_name}',
                                                    callback_data=key_word + Separators.KEY_DATA
                                                                  + group_name + Separators.DATA_META + str(main_data))
        markup.add(getCachedScheduleBtn)

    @staticmethod
    def addCacheTeacherButton(markup: InlineKeyboardMarkup, main_data: int, teacher_name: str, key_word: str,
                            text: str = "Преподаватель"):
        getCachedScheduleBtn = InlineKeyboardButton(text + f' {teacher_name}',
                                                    callback_data=key_word + Separators.KEY_DATA + str(main_data))
        markup.add(getCachedScheduleBtn)

    @staticmethod
    def addPolyLinkGroupButton(markup: InlineKeyboardMarkup):
        getUrlScheduleBtn = InlineKeyboardButton("Сайт с расписанием", url=SCHEDULE_URL)
        markup.add(getUrlScheduleBtn)


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
