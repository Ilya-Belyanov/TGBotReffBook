import datetime

import aiogram.utils.markdown as md

from data.keyspace import LessonsKeyWords
from core import datetimehelper


def beautifySchedule(schedule: list, date: datetime.date):
    even = "чет" if int(date.isocalendar()[1]) % 2 == 0 else "нечет"
    result_str = md.bold("Неделя: ") + datetimehelper.weekRangeStr(date) + " (" + md.bold(even) + ")\n"
    result_str += "-----------------"
    result_str += "\n"
    for day in schedule:
        result_str += md.code(day[LessonsKeyWords.DAY].replace(".", "")) + 2 * "\n"
        for lesson in day[LessonsKeyWords.LESSONS]:
            result_str += md.italic(lesson[LessonsKeyWords.START_TIME]) + " - "
            result_str += md.italic(lesson[LessonsKeyWords.END_TIME])
            result_str += "\n"
            result_str += lesson[LessonsKeyWords.NAME]
            result_str += 2 * "\n"
        result_str += "-----------------"
        result_str += "\n"
    return result_str
