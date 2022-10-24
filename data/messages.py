import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize

from data.commands import COMMANDS


UNKNOWN_MESS = md.text(emojize('Я не знаю, что с этим делать :astonished:'),
                       md.italic('\nЯ просто напомню,'), 'что есть команда', f'/{COMMANDS.HELP}')

COMMANDS_MESS = md.text("Я бот для поиска расписания групп СПбПУ!",
                        "Зайди на главное меню, нажми \"Найти расписание\", выбери необходимые параметры для поиска и "
                        "получи свое расписание",
                        md.bold('Команды:'),
                        "/" + md.italic(COMMANDS.START) + " - Главное меню выбора",
                        "/" + md.italic(COMMANDS.HELP) + " - Информация о боте и вывод всех команд",
                        "/" + md.italic(COMMANDS.PARAMETERS) + " - Текущие введенные параметры", sep='\n')



