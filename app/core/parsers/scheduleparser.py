import json
import datetime
import itertools
from aiohttp import request

from async_lru import alru_cache

from app.data.keyspace import LessonsKeyWords
from app.data.keyspace import Separators
from app.data.urls import SCHEDULE_API_URL


class ScheduleParser:
    """Парсер сайта СПбПУ с расписание с помощью API"""

    @staticmethod
    @alru_cache
    async def getInstitutes() -> dict:
        """API запрос для получения списка всех институтов"""
        url = SCHEDULE_API_URL + f"/faculties"
        async with request("GET", url) as html_page:
            answer = await html_page.json()
            institutes_dict = dict()
            for inst in answer["faculties"]:
                institutes_dict[inst["id"]] = inst["name"]
            return institutes_dict

    @staticmethod
    @alru_cache
    async def getCourses(faculty: int, ed_form: str, degree: int) -> list:
        """API запрос для получения количечества курсов при заданных параметрах"""
        json_pack = await ScheduleParser.getGroups(faculty)
        levels = set()
        for group in json_pack["groups"]:
            if group["type"] == ed_form and group["kind"] == degree:
                levels.add(group['level'])
        return list(levels)

    @staticmethod
    @alru_cache
    async def getGroupsByParameters(faculty: int, ed_form: str, degree: int, level: int) -> dict:
        """API запрос для получения всех групп по парамтерам: институт, форма обучения, степень обучения, курс"""
        json_pack = await ScheduleParser.getGroups(faculty)
        groups = dict()
        for group in json_pack["groups"]:
            if group["type"] == ed_form and group["kind"] == degree and group["level"] == level:
                groups[group["name"] + Separators.DATA_META + str(group["id"])] = group["name"]
        return {i: groups[i] for i in sorted(groups)}

    @staticmethod
    @alru_cache
    async def getGroupsByText(group: str) -> dict:
        """API запрос для получения подходящих групп по тексту"""
        url = SCHEDULE_API_URL + f"/search/groups?q={group}"
        async with request("GET", url) as html_page:
            answer = await html_page.json()
            if answer["groups"] is None:
                return dict()

            groups_dict = dict()
            for gr in answer["groups"]:
                groups_dict[gr["name"] + Separators.DATA_META + str(gr["id"])] = gr["name"]
            return groups_dict

    @staticmethod
    async def getTeacherByTextSlice(teacher: str, start: int, end: int) -> dict:
        groups = await ScheduleParser.getTeacherByText(teacher)
        return dict(itertools.islice(groups.items(), start, end))

    @staticmethod
    @alru_cache
    async def getTeacherNameByID(id: int) -> str:
        """API запрос для получения подходящих преподавателей по тексту"""
        url = SCHEDULE_API_URL + f"/teachers/{id}"
        async with request("GET", url) as html_page:
            answer = await html_page.json()
            if answer.get("error"):
                return str()
            return answer["full_name"]

    @staticmethod
    @alru_cache
    async def getTeacherByText(teacher: str) -> dict:
        """API запрос для получения подходящих преподавателей по тексту"""
        url = SCHEDULE_API_URL + f"/search/teachers?q={teacher}"
        async with request("GET", url) as html_page:
            answer = await html_page.json()
            if answer["teachers"] is None:
                return dict()

            teachers_dict = dict()
            for tcr in answer["teachers"]:
                teachers_dict[str(tcr["id"])] = tcr["full_name"]
            return {i[0]: i[1] for i in sorted(teachers_dict.items(), key=lambda t: t[1])}

    @staticmethod
    @alru_cache
    async def getPlacesByText(place: str) -> dict:
        """API запрос для получения подходящих групп по тексту"""
        url = SCHEDULE_API_URL + f"/search/rooms?q={place}"
        async with request("GET", url) as html_page:
            answer = await html_page.json()
            if answer["rooms"] is None:
                return dict()

            groups_dict = dict()
            for gr in answer["rooms"]:
                groups_dict[str(gr["building"]["id"]) + Separators.DATA_META + str(gr["id"])] = gr["building"]["name"] \
                                                                                                + ", " + gr["name"]
            return groups_dict

    @staticmethod
    @alru_cache
    async def getLessons(group: int, date: datetime.date) -> list:
        """API запрос для получения занятий группы на неделю, где присутсвуте дата = date"""
        url = SCHEDULE_API_URL + '/scheduler/' + str(group) + '?date=' + date.isoformat()
        async with request("GET", url) as html_page:
            answer = await html_page.json()
            return ScheduleParser.parseLessons(answer)

    @staticmethod
    @alru_cache
    async def getTeacherLessons(teacher: int, date: datetime.date) -> list:
        """API запрос для получения занятий преподавателя на неделю, где присутсвуте дата = date"""
        url = SCHEDULE_API_URL + '/teachers/' + str(teacher) + "/scheduler?date=" + date.isoformat()
        async with request("GET", url) as html_page:
            answer = await html_page.json()
            return ScheduleParser.parseLessons(answer)

    @staticmethod
    @alru_cache
    async def getPlaceLessons(building: int, place: int, date: datetime.date) -> list:
        """API запрос для получения занятий преподавателя на неделю, где присутсвуте дата = date"""
        url = SCHEDULE_API_URL + '/buildings/' + str(building) + '/rooms/' + str(place) + "/scheduler?date=" + date.isoformat()
        async with request("GET", url) as html_page:
            answer = await html_page.json()
            return ScheduleParser.parseLessons(answer)

    @staticmethod
    def parseLessons(answer: json) -> list:
        """Парсит json расписания"""
        lessons_result = []
        for day in answer["days"]:
            day_dict = dict()
            day_dict[LessonsKeyWords.DAY] = day["date"]
            lessons_at_day = []
            for lesson in day["lessons"]:
                lesson_dict = dict()
                lesson_dict[LessonsKeyWords.START_TIME] = lesson["time_start"]
                lesson_dict[LessonsKeyWords.END_TIME] = lesson["time_end"]
                lesson_dict[LessonsKeyWords.NAME] = lesson["subject_short"]
                # Type
                if lesson.get("typeObj") is not None:
                    lesson_dict[LessonsKeyWords.TYPE] = lesson.get("typeObj")["name"]

                # Groups
                if lesson.get("groups") is not None:
                    lesson_dict[LessonsKeyWords.GROUPS_NAME] = [group["name"] for group in lesson["groups"]]
                    lesson_dict[LessonsKeyWords.GROUPS_LINK] = [
                        f"/faculty/{group['faculty']['id']}/groups/{group['id']}" for group in lesson["groups"]]

                # Teacher
                if lesson.get("teachers") is not None:
                    lesson_dict[LessonsKeyWords.TEACHER_NAME] = lesson["teachers"][0]["full_name"]
                    lesson_dict[LessonsKeyWords.TEACHER_LINK] = f"/teachers/{lesson['teachers'][0]['id']}"

                # Place
                if lesson.get("auditories") is not None:
                    auditori = lesson["auditories"][0]
                    lesson_dict[LessonsKeyWords.PLACE_NAME] = auditori["building"]["name"] + ", " + auditori["name"]
                    lesson_dict[LessonsKeyWords.PLACE_LINK] = f"/places/{auditori['building']['id']}/{auditori['id']}"

                # Resource
                if lesson.get("lms_url") is not None and lesson.get("lms_url") != "":
                    lesson_dict[LessonsKeyWords.RESOURCE_NAME] = "СДО"
                    lesson_dict[LessonsKeyWords.RESOURCE_LINK] = lesson["lms_url"]
                lessons_at_day.append(lesson_dict)
                day_dict[LessonsKeyWords.LESSONS] = lessons_at_day
            lessons_result.append(day_dict)
        return lessons_result

    @staticmethod
    @alru_cache
    async def getGroups(faculty):
        """API запрос для получения всех групп в институте"""
        group_url = SCHEDULE_API_URL + "faculties/" + str(faculty) + "/groups"
        async with request("GET", group_url) as html_page:
            return await html_page.json()
