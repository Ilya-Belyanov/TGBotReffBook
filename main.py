from aiogram.utils import executor

from bot import dispatcher

# Порядок импортов имеет значение

# Приходим в эти функции из любых состояний (по нажатию на кнопки главного меню)
import menucommands

# Приходим в эти функции из любых состояний (по нажатию на кнопки главных кнопок)
import callbackstartmenu

# Приходим в эти функции из любых состояний (обработка кнопок, например, открыть группу)
import callbackallstates

# Состояние поиска группы по фильтрам
import callbackfilterstate

# Состояние поиска группы по имени
import callbackgroupsearchstate

# Состояние просмотра расписания
import callbacklessonstate

# Не смогли обработать команду (текст или кнопку, так как в другом состоянии)
import unknowncommand

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
