import datetime

from core.parsers.scheduleparser import ScheduleParser
from core.datetimehelper import daysBetweenNow


class ScheduleParserCashManager:
    INSTITUTE_CASH = dict()
    INSTITUTE_LAST_DT_CASH = datetime.datetime.now().date()
    COURSE_LAST_DT_CASH = datetime.datetime.now().date()
    GROUPS_LAST_DT_CASH = datetime.datetime.now().date()
    LESSONS_LAST_DT_CASH = datetime.datetime.now().date()
    CASH_PERIOD = 30

    @classmethod
    async def getInstitutes(cls):
        if len(cls.INSTITUTE_CASH) == 0 or daysBetweenNow(cls.INSTITUTE_LAST_DT_CASH) > cls.CASH_PERIOD:
            cls.INSTITUTE_CASH = await ScheduleParser.getInstitutes()
            cls.INSTITUTE_LAST_DT_CASH = datetime.datetime.now().date()
        return cls.INSTITUTE_CASH

    @classmethod
    async def getCourses(cls, faculty: int, ed_form: str, degree: int):
        if daysBetweenNow(cls.COURSE_LAST_DT_CASH) > cls.CASH_PERIOD:
            ScheduleParser.getCourses.cache_clear()
            cls.COURSE_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getCourses(faculty, ed_form, degree)

    @classmethod
    async def getGroupsByParameters(cls, faculty: int, ed_form: str, degree: int, level: int):
        if daysBetweenNow(cls.GROUPS_LAST_DT_CASH) > cls.CASH_PERIOD:
            ScheduleParser.getGroupsByParameters.cache_clear()
            cls.GROUPS_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getGroupsByParameters(faculty, ed_form, degree, level)

    @classmethod
    async def getLessons(cls, faculty: int, group: int, date: datetime.date):
        if daysBetweenNow(cls.LESSONS_LAST_DT_CASH) > cls.CASH_PERIOD:
            ScheduleParser.getLessons.cache_clear()
            cls.LESSONS_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getLessons(faculty, group, date)

    @classmethod
    async def getInstituteNameByID(cls, id: int):
        inst = await cls.getInstitutes()
        return inst.get(id)

