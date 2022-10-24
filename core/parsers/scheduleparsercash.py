import datetime

from core.parsers.scheduleparser import ScheduleParser
from core.datetimehelper import daysBetweenNow


class ScheduleParserCash:
    INSTITUTE_CASH = dict()
    INSTITUTE_LAST_DT_CASH = datetime.datetime.now().date()
    INSTITUTE_CASH_PERIOD = 30

    @classmethod
    def getInstitutes(cls):
        if len(cls.INSTITUTE_CASH) == 0 or daysBetweenNow(cls.INSTITUTE_LAST_DT_CASH) > cls.INSTITUTE_CASH_PERIOD:
            cls.INSTITUTE_CASH = ScheduleParser.getInstitutes()
            cls.INSTITUTE_LAST_DT_CASH = datetime.datetime.now().date()
        return cls.INSTITUTE_CASH

    @classmethod
    def getCourses(cls, faculty: int, ed_form: str, degree: int):
        return ScheduleParser.getCourses(faculty, ed_form, degree)

    @classmethod
    def getGroupsByParameters(cls, faculty: int, ed_form: str, degree: int, level: int):
        return ScheduleParser.getGroupsByParameters(faculty, ed_form, degree, level)

    @classmethod
    def getLessons(cls, faculty: int, group: int, date: datetime.date):
        return ScheduleParser.getLessons(faculty, group, date)

    @classmethod
    def getInstituteNameByID(cls, id: int):
        inst = cls.getInstitutes()
        return inst.get(id)

