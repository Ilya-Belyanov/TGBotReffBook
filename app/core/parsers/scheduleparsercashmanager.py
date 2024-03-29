import datetime

from app.core.parsers.scheduleparser import ScheduleParser
from app.core.datetimehelper import daysBetweenNow


class ScheduleParserCashManager:
    INSTITUTE_LAST_DT_CASH = datetime.datetime.now().date()
    INSTITUTE_CASH_PERIOD = 30
    COURSE_LAST_DT_CASH = datetime.datetime.now().date()
    COURSE_CASH_PERIOD = 30
    GROUPS_LAST_DT_CASH = datetime.datetime.now().date()
    GROUPS_CASH_PERIOD = 30

    LESSONS_LAST_DT_CASH = datetime.datetime.now().date()
    LESSONS_CASH_PERIOD = 1

    LESSONS_TEACHER_LAST_DT_CASH = datetime.datetime.now().date()
    LESSONS_TEACHER_CASH_PERIOD = 1

    LESSONS_PLACE_LAST_DT_CASH = datetime.datetime.now().date()
    LESSONS_PLACE_CASH_PERIOD = 1

    TEACHER_BY_ID_LAST_DT_CASH = datetime.datetime.now().date()
    TEACHER_BY_ID_CASH_PERIOD = 1

    @classmethod
    async def getInstitutes(cls):
        """С кэшем"""
        if daysBetweenNow(cls.INSTITUTE_LAST_DT_CASH) > cls.INSTITUTE_CASH_PERIOD:
            ScheduleParser.getInstitutes.cache_clear()
            cls.INSTITUTE_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getInstitutes()

    @classmethod
    async def getCourses(cls, faculty: int, ed_form: str, degree: int):
        """С кэшем"""
        if daysBetweenNow(cls.COURSE_LAST_DT_CASH) > cls.COURSE_CASH_PERIOD:
            ScheduleParser.getGroups.cache_clear()
            ScheduleParser.getCourses.cache_clear()
            cls.COURSE_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getCourses(faculty, ed_form, degree)

    @classmethod
    async def getGroupsByParameters(cls, faculty: int, ed_form: str, degree: int, level: int):
        """С кэшем"""
        if daysBetweenNow(cls.GROUPS_LAST_DT_CASH) > cls.GROUPS_CASH_PERIOD:
            ScheduleParser.getGroups.cache_clear()
            ScheduleParser.getGroupsByParameters.cache_clear()
            cls.GROUPS_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getGroupsByParameters(faculty, ed_form, degree, level)

    @classmethod
    async def getGroupsByText(cls, group: str):
        """Без кэша"""
        return await ScheduleParser.getGroupsByText(group)

    @classmethod
    async def getTeacherByText(cls, group: str):
        """Без кэша"""
        return await ScheduleParser.getTeacherByText(group)

    @classmethod
    async def getPlacesByText(cls, place: str):
        """Без кэша"""
        return await ScheduleParser.getPlacesByText(place)

    @classmethod
    async def getLessons(cls, group: int, date: datetime.date):
        """С кэшем"""
        if daysBetweenNow(cls.LESSONS_LAST_DT_CASH) > cls.LESSONS_CASH_PERIOD:
            ScheduleParser.getLessons.cache_clear()
            cls.LESSONS_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getLessons(group, date)

    @classmethod
    async def getTeacherLessons(cls, teacher: int, date: datetime.date):
        """С кэшем"""
        if daysBetweenNow(cls.LESSONS_TEACHER_LAST_DT_CASH) > cls.LESSONS_TEACHER_CASH_PERIOD:
            ScheduleParser.getTeacherLessons.cache_clear()
            cls.LESSONS_TEACHER_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getTeacherLessons(teacher, date)

    @classmethod
    async def getPlaceLessons(cls, building: int, place: int, date: datetime.date):
        """С кэшем"""
        if daysBetweenNow(cls.LESSONS_PLACE_LAST_DT_CASH) > cls.LESSONS_PLACE_CASH_PERIOD:
            ScheduleParser.getPlaceLessons.cache_clear()
            cls.LESSONS_PLACE_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getPlaceLessons(building, place, date)

    @classmethod
    async def getInstituteNameByID(cls, id: int):
        inst = await cls.getInstitutes()
        return inst.get(id)

    @classmethod
    async def getTeacherNameByID(cls, id: int):
        """С кэшем"""
        if daysBetweenNow(cls.TEACHER_BY_ID_LAST_DT_CASH) > cls.TEACHER_BY_ID_CASH_PERIOD:
            ScheduleParser.getTeacherNameByID.cache_clear()
            cls.TEACHER_BY_ID_LAST_DT_CASH = datetime.datetime.now().date()
        return await ScheduleParser.getTeacherNameByID(id)

    @classmethod
    async def clearCache(cls):
        ScheduleParser.getInstitutes.cache_clear()
        ScheduleParser.getGroups.cache_clear()
        ScheduleParser.getCourses.cache_clear()
        ScheduleParser.getGroupsByParameters.cache_clear()
        ScheduleParser.getLessons.cache_clear()
        ScheduleParser.getTeacherLessons.cache_clear()
        ScheduleParser.getPlaceLessons.cache_clear()
        ScheduleParser.getTeacherNameByID.cache_clear()
