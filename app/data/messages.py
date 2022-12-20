import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize

from app.data.commands import COMMANDS


UNKNOWN_MESS = md.text(emojize('Я не знаю, что с этим делать :astonished:'),
                       md.italic('\nЯ просто напомню,'), 'что есть команда', f'/{COMMANDS.HELP}')

COMMANDS_MESS = md.text("Я бот по поиску расписания для групп, преподавателей и аудиторий СПбПУ!",
                        "Зайдите на главное меню, нажми \"Найти расписание\", чтобы найти группу по фильтрам.",
                        "'Поиск по группе' - введите номер группы и нажмите на нужную из результата поиска для "
                        "получения расписания.",
                        "'Поиск по преподавателю' - введите имя преподавателя и выберите нужного.",
                        "'Поиск по аудитории' - введите имя аудитории (например: 'В2.02').",
                        "При просмотре расписания введите дату в формате 'dd', 'ddmm' или 'ddmmyy' для поиска "
                        "расписания на неделю с этой датой."
                        "Почта технической поддержки " + md.italic("support@spbstu.ru"),
                        md.bold('Команды:'),
                        "/" + md.italic(COMMANDS.START) + " - Главное меню выбора",
                        "/" + md.italic(COMMANDS.HELP) + " - Информация о боте и всех командах",
                        "/" + md.italic(COMMANDS.SAVED) + " - Сохраненные и последние поиски",
                        "/" + md.italic(COMMANDS.PARAMETERS) + " - Текущие введенные параметры", sep='\n')



