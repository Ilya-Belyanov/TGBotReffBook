from aiogram.utils import executor

from app.bot import dispatcher
from app.core.dbhelper import db_connect
from app.core.googleanalytics import send_analytics

# Порядок импортов имеет значение

# Приходим в эти функции из любых состояний (по нажатию на кнопки главного меню)
import app.bottriggers.menucommands

# Приходим в эти функции из любых состояний (по нажатию на кнопки главных кнопок)
import app.bottriggers.callbackstartmenu

"""Обработка нажатий из панели админа"""
import app.bottriggers.callbackadminmenu

# Приходим в эти функции из любых состояний (обработка кнопок, например, открыть группу)
import app.bottriggers.callbackallstates

# Состояние поиска группы по фильтрам
import app.bottriggers.callbackfilterstate

# Состояние поиска группы по имени
import app.bottriggers.callbackgroupsearchstate

# Состояние поиска преподавателя по имени
import app.bottriggers.callbackteachersearchstate

# Состояние поиска преподавателя по имени
import app.bottriggers.callbackplacesearchstate

"""Отослать сообщение всем людям"""
import app.bottriggers.callbackwritetoall

'''Состояние просмотра расписания'''
import app.bottriggers.callbacklessonstate

# Не смогли обработать команду (текст или кнопку, так как в другом состоянии)
import app.bottriggers.unknowncommand


async def on_start_bot(_):
    await db_connect("db.db")
    await send_analytics(0, "START_BOT")


if __name__ == "__main__":
    executor.start_polling(dispatcher,
                           skip_updates=True,
                           on_startup=on_start_bot)
