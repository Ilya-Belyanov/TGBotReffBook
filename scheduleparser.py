import datetime

import requests
from bs4 import BeautifulSoup as bs

from data import LessonsKeyWords


class ScheduleParser:
    BASE_URL = 'https://ruz.spbstu.ru'

    @staticmethod
    def getInstitutes():
        htlm_page = requests.get(ScheduleParser.BASE_URL)
        print("Status Code: ", htlm_page.status_code)

        soup = bs(htlm_page.text)

        institutes = soup.findAll(name='li', class_='faculty-list__item')
        institutes_dict = dict()

        for inst in institutes:
            faculty = inst.find(name='a', class_='faculty-list__link')
            code = int(faculty['href'].split('/')[2])
            institutes_dict[code] = faculty.text
        return institutes_dict

    @staticmethod
    def getCourses(faculty: int, ed_form: str, degree: int):
        json_pack = ScheduleParser.getGroups(faculty)
        levels = set()
        for group in json_pack["groups"]:
            if group["type"] == ed_form and group["kind"] == degree:
                levels.add(group['level'])
        return list(levels)

    @staticmethod
    def getGroupsByParameters(faculty: int, ed_form: str, degree: int, level: int):
        json_pack = ScheduleParser.getGroups(faculty)
        groups = dict()
        for group in json_pack["groups"]:
            if group["type"] == ed_form and group["kind"] == degree and group["level"] == level:
                groups[group["name"] + "|" + str(group["id"])] = group["name"]
        return {i: groups[i] for i in sorted(groups)}

    @staticmethod
    def getLessons(faculty: int, group: int, date: datetime.date):
        url = ScheduleParser.BASE_URL + '/faculty/' + str(faculty) + '/groups/' + str(
            group) + '?date=' + date.isoformat()

        htlm_inf = requests.get(url)
        print("Status Code: ", htlm_inf.status_code)
        soup = bs(htlm_inf.text)
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
                lessons_at_day.append(lesson_dict)
            day_dict[LessonsKeyWords.LESSONS] = lessons_at_day
            lessons_result.append(day_dict)
        return lessons_result

    @staticmethod
    def getGroups(faculty):
        group_url = ScheduleParser.BASE_URL + "/api/v1/ruz/faculties/" + str(faculty) + "/groups"
        return requests.get(group_url).json()
