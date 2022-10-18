import datetime

import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize

from data import LessonsKeyWords
import datetimehelper


class COMMANDS:
    START = 'start'
    HELP = 'help'


UNKNOWN_MESS = md.text(emojize('Я не знаю, что с этим делать :astonished:'),
                       md.italic('\nЯ просто напомню,'), 'что есть команда', '/help')

COMMANDS_MESS = md.text(md.bold('Команды:'),
                        "/" + md.italic(COMMANDS.START) + " - Главное меню выбора",
                        "/" + md.italic(COMMANDS.HELP) + " - Вывод всех команд", sep='\n')


def parseForData(data: str):
    return data.split(":")[1]


def beautifySchedule(schedule: list, date: datetime.date):
    even = "чет" if int(date.isocalendar()[1]) % 2 == 0 else "нечет"
    result_str = md.bold("Неделя: ") + datetimehelper.weekRangeStr(date) + " (" + md.bold(even) + ")\n"
    result_str += "-----------------"
    result_str += "\n"
    for day in schedule:
        result_str += md.code(day[LessonsKeyWords.DAY].replace(".", "")) + 2 * "\n"
        for lesson in day[LessonsKeyWords.LESSONS]:
            result_str += md.italic(lesson[LessonsKeyWords.START_TIME]) + " - " + md.italic(lesson[LessonsKeyWords.END_TIME])
            result_str += "\n"
            result_str += lesson[LessonsKeyWords.NAME]
            result_str += 2 * "\n"
        result_str += "-----------------"
        result_str += "\n"
    return result_str



