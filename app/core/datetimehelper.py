import datetime

WEEKDAYS = {0: "пн", 1: "вт", 2: "ср", 3: "чт", 4: "пт", 5: "сб", 6: "вс"}
MONTHS = {1: "янв", 2: "фев", 3: "март", 4: "апр", 5: "май", 6: "июнь", 7: "июль",
          8: "авг", 9: "сен", 10: "окт", 11: "нояб", 12: "дек"}


def startDayOfWeek(date: datetime.date) -> datetime.date:
    return date - datetime.timedelta(days=(date.isoweekday() % 7) - 1)


def createPrevNextWeeks(date: datetime.date) -> dict:
    result = dict()
    for i in [-1, 1]:
        dt_prev = startDayOfWeek(date + datetime.timedelta(7 * i))
        result[dt_prev] = dt_prev.strftime("%d %m") + " - " + (dt_prev + datetime.timedelta(6)).strftime("%d %m")
    return result


def weekRangeStr(date: datetime.date) -> str:
    return date.strftime("%d %m") + " - " + (date + datetime.timedelta(6)).strftime("%d %m")


def isEvenWeek(date: datetime.date) -> bool:
    return int(date.isocalendar()[1]) % 2 == 0


def isDayTime(time: datetime.time):
    return 6 <= time.hour < 18


def daysBetween(start: datetime.date, end: datetime.date):
    return abs((end - start).days)


def daysBetweenNow(date: datetime.date):
    return daysBetween(date, datetime.datetime.now().date())


def weekday_str(date: datetime.date):
    return WEEKDAYS[date.weekday()]


def month_str(date: datetime.date):
    return MONTHS[date.month]


def strToDate(string: str):
    today = datetime.date.today()
    date_obj = datetime.datetime.today()
    try:
        if len(string) == 2:
            date_obj = datetime.datetime.strptime(string, '%d')
            date_obj = date_obj.replace(month=today.month, year=today.year)
        elif len(string) == 4:
            date_obj = datetime.datetime.strptime(string, '%d%m')
            date_obj = date_obj.replace(year=today.year)
        elif len(string) == 6:
            date_obj = datetime.datetime.strptime(string, '%d%m%y')
        else:
            return today, False
    except Exception as e:
        print(e)
        return today, False
    return date_obj.date(), True
