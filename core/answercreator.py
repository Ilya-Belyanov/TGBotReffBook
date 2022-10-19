import datetime

import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize

import data.emojizedb as edb
from data.keyspace import LessonsKeyWords
from data.urls import SCHEDULE_URL
from core import datetimehelper


def beautifySchedule(schedule: list, date: datetime.date):
    result_list = []
    even = "чет" if datetimehelper.isEvenWeek(date) else "нечет"
    result_str = md.bold("Неделя: ") + datetimehelper.weekRangeStr(date).replace("-", "\-") + " \(" + md.bold(
        even) + "\)\n"
    result_list.append(result_str)
    result_str = ""
    for day in schedule:
        result_str += md.code(day[LessonsKeyWords.DAY]) + 2 * "\n"
        for lesson in day[LessonsKeyWords.LESSONS]:
            result_str += md.italic(lesson[LessonsKeyWords.START_TIME]) + " \- "
            result_str += md.italic(lesson[LessonsKeyWords.END_TIME])
            result_str += "\n"
            result_str += md.bold(lesson[LessonsKeyWords.NAME])
            result_str += "\n"
            result_str += emojize(f"{edb.FACE_WITH_MONOCLE} ") + md.link(lesson[LessonsKeyWords.TEACHER_NAME],
                                                                         SCHEDULE_URL + lesson[LessonsKeyWords.TEACHER_LINK])
            result_str += "\n"
            result_str += emojize(f"{edb.SCHOOL} ") + md.link(lesson[LessonsKeyWords.PLACE_NAME],
                                               SCHEDULE_URL + lesson[LessonsKeyWords.PLACE_LINK])

            if LessonsKeyWords.RESOURCE_NAME in lesson:
                result_str += "\n"
                result_str += emojize(f"{edb.FILE_FOLDER} ") + md.link(lesson[LessonsKeyWords.RESOURCE_NAME],
                                                      lesson[LessonsKeyWords.RESOURCE_LINK])
            result_str += 2 * "\n"
        result_list.append(result_str)
        result_str = ""
    if len(schedule) == 0:
        result_list.append(emojize(f"{edb.GRIN} ") + md.code("На этой неделе можно отдохнуть\!"))
    return result_list