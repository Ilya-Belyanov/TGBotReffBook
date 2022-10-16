import requests
from bs4 import BeautifulSoup as bs


class ScheduleParser:
    BASE_URL = 'https://ruz.spbstu.ru'

    @staticmethod
    def getInstitutes():
        htlm_page = requests.get(ScheduleParser.BASE_URL)
        print("Status Code: ", htlm_page.status_code)

        # Переводим полученный ответ в текст и размечаем его по тегам
        soup = bs(htlm_page.text)

        # Извлекаем нужную информацию
        institutes = soup.findAll(name='li', class_='faculty-list__item')
        institutes_dict = dict()

        for inst in institutes:
            faculty = inst.find(name='a', class_='faculty-list__link')
            code = int(faculty['href'].split('/')[2])
            name = faculty.text
            institutes_dict[code] = name
        return institutes_dict

    @staticmethod
    def getCourses(group: int):
        group_url = ScheduleParser.BASE_URL + "/faculty/" + str(group) + "/groups"
        htlm_page = requests.get(group_url)
        print("Status Code: ", htlm_page.status_code)

        # Переводим полученный ответ в текст и размечаем его по тегам
        soup = bs(htlm_page.text)

        # Извлекаем нужную информацию
        levels = soup.findAll(name='div', class_='faculty__level')
        levels_list = []

        for level in levels:
            faculty = level.find(name='h3')
            levels_list.append(faculty.text)
        return levels_list

