import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize


class COMMANDS:
    START = '/start'
    HELP = '/help'
    CHANGE_STATE = '/change'


UNKNOWN_MESS = md.text(emojize('Я не знаю, что с этим делать :astonished:'),
                       md.italic('\nЯ просто напомню,'), 'что есть команда', '/help')

COMMANDS_MESS = md.text(md.bold('Команды:'),
                        md.italic(COMMANDS.START) + " - Приветствие",
                        md.italic(COMMANDS.CHANGE_STATE) + " - Изменить состояние",
                        md.italic(COMMANDS.HELP) + " - Вывод всех команд", sep='\n')


class STD_STATE:
    NAME_STATE = "state_std"
    START = "Привет!\nНапиши мне что-нибудь!"
    HELP = emojize('Напиши мне, и я отправлю этот текст тебе в ответ:smirk:!')


class STATE_0:
    NAME_STATE = "state_0"
    START = "ООО!\nя так бодр..."
    HELP = 'Не пиши мне!'


class STATE_1:
    NAME_STATE = "state_1"
    START = "Отстань!\nя устал..."
    HELP = STATE_0.HELP
