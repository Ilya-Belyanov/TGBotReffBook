import datetime


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
