import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize


class COMMANDS:
    START = 'start'
    HELP = '/help'


UNKNOWN_MESS = md.text(emojize('Я не знаю, что с этим делать :astonished:'),
                       md.italic('\nЯ просто напомню,'), 'что есть команда', '/help')

COMMANDS_MESS = md.text(md.bold('Команды:'),
                        md.italic(COMMANDS.START) + " - Приветствие",
                        md.italic(COMMANDS.HELP) + " - Вывод всех команд", sep='\n')
