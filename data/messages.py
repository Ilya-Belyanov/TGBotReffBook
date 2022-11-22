import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize

from data.commands import COMMANDS


UNKNOWN_MESS = md.text(emojize('Я не знаю, что с этим делать :astonished:'),
                       md.italic('\nЯ просто напомню,'), 'что есть команда', f'/{COMMANDS.HELP}')

COMMANDS_MESS = md.text("Я бот для поиска расписания для групп, преподавателей и аудиторий СПбПУ!",
                        "Зайди на главное меню, нажми \"Найти расписание\", чтобы найти группу по фильтрам",
                        "Для поиска группы по номеру - выбери 'Поиск по группе'",
                        "Для поиска преподавателя по имени - выбери 'Поиск по преподавателю'",
                        "Для поиска аудитории по названию - выбери 'Поиск по аудитории'",
                        "Почта технической поддержки " + md.italic("support@spbstu.ru"),
                        md.bold('Команды:'),
                        "/" + md.italic(COMMANDS.START) + " - Главное меню выбора",
                        "/" + md.italic(COMMANDS.HELP) + " - Информация о боте и вывод всех команд",
                        "/" + md.italic(COMMANDS.SAVED) + " - Сохраненные и последние поиски",
                        "/" + md.italic(COMMANDS.PARAMETERS) + " - Текущие введенные параметры", sep='\n')



