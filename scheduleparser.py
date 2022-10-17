import requests
from bs4 import BeautifulSoup as bs


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
                groups[group["id"]] = group["name"]
        return {i: groups[i] for i in sorted(groups)}

    @staticmethod
    def getGroups(faculty):
        group_url = ScheduleParser.BASE_URL + "/api/v1/ruz/faculties/" + str(faculty) + "/groups"
        return requests.get(group_url).json()

