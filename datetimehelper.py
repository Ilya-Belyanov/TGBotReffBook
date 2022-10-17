import datetime


def startDayOfWeek(date):
    return date - datetime.timedelta(days=(date.isoweekday() % 7) - 1)


def formeThreeWeekRange(date):
    result = dict()
    for i in range(-1, 2):
        dt = startDayOfWeek(date + datetime.timedelta(7 * i))
        result[dt] = dt.strftime("%d %m") + " - " + (dt + datetime.timedelta(6)).strftime("%d %m")
    return result
