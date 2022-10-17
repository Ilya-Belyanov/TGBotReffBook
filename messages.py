import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize

from data import LessonsKeyWords


class COMMANDS:
    START = 'start'
    HELP = 'help'


UNKNOWN_MESS = md.text(emojize('Я не знаю, что с этим делать :astonished:'),
                       md.italic('\nЯ просто напомню,'), 'что есть команда', '/help')

COMMANDS_MESS = md.text(md.bold('Команды:'),
                        md.italic(COMMANDS.START) + " - Приветствие",
                        md.italic(COMMANDS.HELP) + " - Вывод всех команд", sep='\n')


def beautifySchedule(schedule: list):
    result_str = ""
    for day in schedule:
        result_str += day[LessonsKeyWords.DAY] + 2 * "\n"
        for lesson in day[LessonsKeyWords.LESSONS]:
            result_str += lesson[LessonsKeyWords.START_TIME] + " - " + lesson[LessonsKeyWords.END_TIME]
            result_str += "\n"
            result_str += lesson[LessonsKeyWords.NAME]
            result_str += 2 * "\n"
        result_str += "-----------------"
        result_str += "\n"
    return result_str



