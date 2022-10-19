import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize

from data.commands import COMMANDS


UNKNOWN_MESS = md.text(emojize('Я не знаю, что с этим делать :astonished:'),
                       md.italic('\nЯ просто напомню,'), 'что есть команда', '/help')

COMMANDS_MESS = md.text(md.bold('Команды:'),
                        "/" + md.italic(COMMANDS.START) + " - Главное меню выбора",
                        "/" + md.italic(COMMANDS.HELP) + " - Вывод всех команд", sep='\n')



