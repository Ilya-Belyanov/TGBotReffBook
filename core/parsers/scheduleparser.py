import json
import datetime
import itertools
from aiohttp import request

from async_lru import alru_cache
from bs4 import BeautifulSoup as bs

from data.keyspace import LessonsKeyWords
from data.keyspace import Separators
from data.urls import SCHEDULE_URL, SCHEDULE_API_URL


class ScheduleParser:
    @staticmethod
    async def getInstitutes() -> dict:
        async with request("GET", SCHEDULE_URL) as html_page:
            text = await html_page.text()
            soup = bs(text, features="html.parser")

            institutes = soup.findAll(name='li', class_='faculty-list__item')
            institutes_dict = dict()

            for inst in institutes:
                faculty = inst.find(name='a', class_='faculty-list__link')
                code = int(faculty['href'].split('/')[2])
                institutes_dict[code] = faculty.text
            return institutes_dict

    @staticmethod
    @alru_cache
    async def getCourses(faculty: int, ed_form: str, degree: int) -> list:
        json_pack = await ScheduleParser.getGroups(faculty)
        levels = set()
        for group in json_pack["groups"]:
            if group["type"] == ed_form and group["kind"] == degree:
                levels.add(group['level'])
        return list(levels)

    @staticmethod
    @alru_cache
    async def getGroupsByParameters(faculty: int, ed_form: str, degree: int, level: int) -> dict:
        json_pack = await ScheduleParser.getGroups(faculty)
        groups = dict()
        for group in json_pack["groups"]:
            if group["type"] == ed_form and group["kind"] == degree and group["level"] == level:
                groups[group["name"] + Separators.DATA_META + str(group["id"])] = group["name"]
        return {i: groups[i] for i in sorted(groups)}

    @staticmethod
    @alru_cache
    async def getGroupsByText(group: str) -> dict:
        url = SCHEDULE_URL + f"/search/groups?q={group}"
        async with request("GET", url) as html_page:
            text = await html_page.text()
            soup = bs(text, features="html.parser")

            groups = soup.findAll(name='li', class_='groups-list__item')
            groups_dict = dict()

            for gr in groups:
                gr_item = gr.find(name='a', class_='groups-list__link')
                id_item = int(gr_item['href'].split('/')[4])
                groups_dict[gr_item.text + Separators.DATA_META + str(id_item)] = gr_item.text
            return groups_dict

    @staticmethod
    async def getTeacherByTextSlice(teacher: str, start: int, end: int) -> dict:
        groups = await ScheduleParser.getTeacherByText(teacher)
        return dict(itertools.islice(groups.items(), start, end))

    @staticmethod
    @alru_cache
    async def getTeacherByText(teacher: str) -> dict:
        url = SCHEDULE_URL + f"/search/teacher?q={teacher}"
        async with request("GET", url) as html_page:
            text = await html_page.text()
            soup = bs(text, features="html.parser")

            groups = soup.find(name='body').find(name='script')
            js = groups.text.split("=")[1][:-1]
            js = js.split("persist")[0][:-2] + "}"
            js_ob = json.loads(js)

            groups_dict = dict()

            for gr in js_ob["searchTeacher"]["data"]:
                groups_dict[str(gr["id"])] = gr["full_name"]
            return groups_dict

    @staticmethod
    @alru_cache
    async def getTeacherLessons(teacher: int, date: datetime.date) -> list:
        url = SCHEDULE_URL + '/teachers/' + str(teacher) + '?date=' + date.isoformat()
        print(url)
        async with request("GET", url) as html_page:
            text = await html_page.text()
            return ScheduleParser.parseLessons(text)

    @staticmethod
    @alru_cache
    async def getLessons(group: int, date: datetime.date) -> list:
        url = SCHEDULE_URL + '/faculty/' + str(94) + '/groups/' + str(
            group) + '?date=' + date.isoformat()
        async with request("GET", url) as html_page:
            text = await html_page.text()
            return ScheduleParser.parseLessons(text)

    @staticmethod
    def parseLessons(text: str) -> list:
        """Парсит текст расписания"""

        soup = bs(text, features="html.parser")
        days = soup.find(name='ul', class_='schedule').findAll(name='li', class_='schedule__day')

        lessons_result = []
        for day in days:
            day_dict = {}
            day_item = day.find(name='div', class_='schedule__date')
            day_dict[LessonsKeyWords.DAY] = day_item.text
            lessons = day.findAll(name='li', class_='lesson')
            lessons_at_day = []
            for lesson in lessons:
                lesson_dict = dict()
                lesson_item = lesson.find(name='div', class_='lesson__subject').findAll(name='span')
                lesson_dict[LessonsKeyWords.START_TIME] = lesson_item[1].text
                lesson_dict[LessonsKeyWords.END_TIME] = lesson_item[3].text
                lesson_dict[LessonsKeyWords.NAME] = lesson_item[5].text

                # Type
                lesson_type = lesson.find(name='div', class_='lesson__type')
                if lesson_type is not None:
                    lesson_dict[LessonsKeyWords.TYPE] = lesson_type.text

                # Groups
                lesson_groups = lesson.find(name='div', class_='lesson-groups__list')
                if lesson_groups is not None:
                    lesson_groups = lesson_groups.findAll(name='a', class_='lesson__link')
                    lesson_dict[LessonsKeyWords.GROUPS_NAME] = [group.text for group in lesson_groups]
                    lesson_dict[LessonsKeyWords.GROUPS_LINK] = [group['href'] for group in lesson_groups]

                # Teacher
                lesson_teacher = lesson.find(name='div', class_='lesson__teachers')
                if lesson_teacher is not None:
                    lesson_teacher = lesson_teacher.find(name='a', class_='lesson__link')
                    lesson_dict[LessonsKeyWords.TEACHER_NAME] = lesson_teacher.findAll(name='span')[2].text
                    lesson_dict[LessonsKeyWords.TEACHER_LINK] = lesson_teacher['href']

                # Place
                lesson_place = lesson.find(name='div', class_='lesson__places')
                if lesson_place is not None:
                    lesson_place = lesson_place.find(name='a', class_='lesson__link')
                    place_spans = lesson_place.findAll(name='span')
                    lesson_dict[LessonsKeyWords.PLACE_NAME] = place_spans[0].text + " " + place_spans[5].text
                    lesson_dict[LessonsKeyWords.PLACE_LINK] = lesson_place['href']

                # Resource
                lesson_resource = lesson.find(name='div', class_='lesson__resource_links')
                if lesson_resource is not None:
                    resource_link = lesson_resource.find(name='a')
                    lesson_dict[LessonsKeyWords.RESOURCE_NAME] = resource_link.text
                    lesson_dict[LessonsKeyWords.RESOURCE_LINK] = resource_link['href']

                lessons_at_day.append(lesson_dict)
            day_dict[LessonsKeyWords.LESSONS] = lessons_at_day
            lessons_result.append(day_dict)
        return lessons_result

    @staticmethod
    @alru_cache
    async def getGroups(faculty):
        group_url = SCHEDULE_API_URL + "faculties/" + str(faculty) + "/groups"
        async with request("GET", group_url) as html_page:
            return await html_page.json()
