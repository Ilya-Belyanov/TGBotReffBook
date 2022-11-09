from aiogram.utils import executor

from bot import dispatcher

# Порядок импортов имеет значение

# Приходим в эти функции из любых состояний (по нажатию на кнопки главного меню)
import bottriggers.menucommands

# Приходим в эти функции из любых состояний (по нажатию на кнопки главных кнопок)
import bottriggers.callbackstartmenu

# Приходим в эти функции из любых состояний (обработка кнопок, например, открыть группу)
import bottriggers.callbackallstates

# Состояние поиска группы по фильтрам
import bottriggers.callbackfilterstate

# Состояние поиска группы по имени
import bottriggers.callbackgroupsearchstate

# Состояние поиска преподавателя по имени
import bottriggers.callbackteachersearchstate

# Состояние поиска преподавателя по имени
import bottriggers.callbackplacesearchstate

'''Состояние просмотра расписания'''
import bottriggers.callbacklessonstate

# Не смогли обработать команду (текст или кнопку, так как в другом состоянии)
import bottriggers.unknowncommand

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
