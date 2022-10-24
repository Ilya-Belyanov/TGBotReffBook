import datetime
from aiohttp import request

from async_lru import alru_cache
from bs4 import BeautifulSoup as bs

from data.keyspace import LessonsKeyWords
from data.keyspace import Separators
from data.urls import SCHEDULE_URL, SCHEDULE_API_URL


class ScheduleParser:
    @staticmethod
    async def getInstitutes():
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
    async def getCourses(faculty: int, ed_form: str, degree: int):
        json_pack = await ScheduleParser.getGroups(faculty)
        levels = set()
        for group in json_pack["groups"]:
            if group["type"] == ed_form and group["kind"] == degree:
                levels.add(group['level'])
        return list(levels)

    @staticmethod
    @alru_cache
    async def getGroupsByParameters(faculty: int, ed_form: str, degree: int, level: int):
        json_pack = await ScheduleParser.getGroups(faculty)
        groups = dict()
        for group in json_pack["groups"]:
            if group["type"] == ed_form and group["kind"] == degree and group["level"] == level:
                groups[group["name"] + Separators.DATA_META + str(group["id"])] = group["name"]
        return {i: groups[i] for i in sorted(groups)}

    @staticmethod
    @alru_cache
    async def getLessons(faculty: int, group: int, date: datetime.date):
        url = SCHEDULE_URL + '/faculty/' + str(faculty) + '/groups/' + str(
            group) + '?date=' + date.isoformat()
        async with request("GET", url) as html_page:
            text = await html_page.text()
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
    async def getGroups(faculty):
        group_url = SCHEDULE_API_URL + "faculties/" + str(faculty) + "/groups"
        async with request("GET", group_url) as html_page:
            return await html_page.json()
