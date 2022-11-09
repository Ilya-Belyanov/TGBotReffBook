import datetime

from core.parsers.scheduleparser import ScheduleParser
from core.datetimehelper import daysBetweenNow


class ScheduleParserCashManager:
    INSTITUTE_LAST_DT_CASH = datetime.datetime.now().date()
    INSTITUTE_CASH_PERIOD = 30
    COURSE_LAST_DT_CASH = datetime.datetime.now().date()
    COURSE_CASH_PERIOD = 30
    GROUPS_LAST_DT_CASH = datetime.datetime.now().date()
    GROUPS_CASH_PERIOD = 30
    GROUPS_SEARCH_LAST_DT_CASH = datetime.datetime.now().date()
    GROUPS_SEARCH_CASH_PERIOD = 2
    TEACHER_SEARCH_LAST_DT_CASH = datetime.datetime.now().date()
    TEACHER_SEARCH_CASH_PERIOD = 2
    LESSONS_LAST_DT_CASH = datetime.datetime.now().date()
    LESSONS_CASH_PERIOD = 1
    LESSONS_TEACHER_LAST_DT_CASH = datetime.datetime.now().date()
    LESSONS_TEACHER_CASH_PERIOD = 1

    @classmethod
    async def getInstitutes(cls):
        if daysBetweenNow(cls.INSTITUTE_LAST_DT_CASH) > cls.INSTITUTE_CASH_PERIOD:
            ScheduleParser.getInstitutes.cache_clear()
            cls.INSTITUTE_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getInstitutes()

    @classmethod
    async def getCourses(cls, faculty: int, ed_form: str, degree: int):
        if daysBetweenNow(cls.COURSE_LAST_DT_CASH) > cls.COURSE_CASH_PERIOD:
            ScheduleParser.getGroups.cache_clear()
            ScheduleParser.getCourses.cache_clear()
            cls.COURSE_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getCourses(faculty, ed_form, degree)

    @classmethod
    async def getGroupsByParameters(cls, faculty: int, ed_form: str, degree: int, level: int):
        if daysBetweenNow(cls.GROUPS_LAST_DT_CASH) > cls.GROUPS_CASH_PERIOD:
            ScheduleParser.getGroups.cache_clear()
            ScheduleParser.getGroupsByParameters.cache_clear()
            cls.GROUPS_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getGroupsByParameters(faculty, ed_form, degree, level)

    @classmethod
    async def getGroupsByText(cls, group: str):
        if daysBetweenNow(cls.GROUPS_SEARCH_LAST_DT_CASH) > cls.GROUPS_SEARCH_CASH_PERIOD:
            ScheduleParser.getGroupsByText.cache_clear()
            cls.GROUPS_SEARCH_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getGroupsByText(group)

    @classmethod
    async def getTeacherByTextSlice(cls, group: str, start: int, end: int):
        if daysBetweenNow(cls.TEACHER_SEARCH_LAST_DT_CASH) > cls.TEACHER_SEARCH_CASH_PERIOD:
            ScheduleParser.getTeacherByText.cache_clear()
            cls.TEACHER_SEARCH_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getTeacherByTextSlice(group, start, end)

    @classmethod
    async def getTeacherByText(cls, group: str):
        if daysBetweenNow(cls.TEACHER_SEARCH_LAST_DT_CASH) > cls.TEACHER_SEARCH_CASH_PERIOD:
            ScheduleParser.getTeacherByText.cache_clear()
            cls.TEACHER_SEARCH_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getTeacherByText(group)

    @classmethod
    async def getLessons(cls, group: int, date: datetime.date):
        if daysBetweenNow(cls.LESSONS_LAST_DT_CASH) > cls.LESSONS_CASH_PERIOD:
            ScheduleParser.getLessons.cache_clear()
            cls.LESSONS_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getLessons(group, date)

    @classmethod
    async def getTeacherLessons(cls, teacher: int, date: datetime.date):
        if daysBetweenNow(cls.LESSONS_TEACHER_LAST_DT_CASH) > cls.LESSONS_TEACHER_CASH_PERIOD:
            ScheduleParser.getTeacherLessons.cache_clear()
            cls.LESSONS_TEACHER_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getTeacherLessons(teacher, date)

    @classmethod
    async def getInstituteNameByID(cls, id: int):
        inst = await cls.getInstitutes()
        return inst.get(id)

