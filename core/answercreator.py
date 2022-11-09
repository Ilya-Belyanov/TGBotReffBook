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
    result_str = md.bold(f"Неделя: {datetimehelper.weekRangeStr(date)} ({even})\n")
    result_list.append(result_str)
    result_str = ""
    for day in schedule:
        day_lessons = datetime.datetime.strptime(day[LessonsKeyWords.DAY], "%Y-%m-%d")

        result_str += md.code(day_lessons.strftime("%d ") + datetimehelper.month_str(day_lessons) + ", " + datetimehelper.weekday_str(day_lessons)) + 2 * "\n"
        for lesson in day[LessonsKeyWords.LESSONS]:
            result_str += md.italic(lesson[LessonsKeyWords.START_TIME]) + " \- "
            result_str += md.italic(lesson[LessonsKeyWords.END_TIME])
            result_str += "\n"
            result_str += md.bold(lesson[LessonsKeyWords.NAME])

            # Тип занятия
            if LessonsKeyWords.TYPE in lesson:
                result_str += "\n"
                result_str += emojize(f"{edb.LOWER_LEFT_FOUNTAIN_PEN} ")
                result_str += lesson[LessonsKeyWords.TYPE]

            # Группы
            if LessonsKeyWords.GROUPS_NAME in lesson:
                result_str += "\n"
                result_str += emojize(f"{edb.HATCHING_CHICK} ")
                for i, group in enumerate(lesson[LessonsKeyWords.GROUPS_NAME]):
                    result_str += md.link(group, SCHEDULE_URL
                                          + lesson[LessonsKeyWords.GROUPS_LINK][i])
                    if i != len(lesson[LessonsKeyWords.GROUPS_NAME]) - 1:
                        result_str += ", "

            # Учителя
            if LessonsKeyWords.TEACHER_NAME in lesson:
                result_str += "\n"
                result_str += emojize(f"{edb.FACE_WITH_MONOCLE} ") + md.link(lesson[LessonsKeyWords.TEACHER_NAME],
                                                                             SCHEDULE_URL
                                                                             + lesson[LessonsKeyWords.TEACHER_LINK])
            # Место
            if LessonsKeyWords.PLACE_NAME in lesson:
                result_str += "\n"
                result_str += emojize(f"{edb.SCHOOL} ") + md.link(lesson[LessonsKeyWords.PLACE_NAME],
                                                                  SCHEDULE_URL + lesson[LessonsKeyWords.PLACE_LINK])

            # Ресурс
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
