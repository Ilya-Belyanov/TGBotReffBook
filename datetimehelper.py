import datetime


def startDayOfWeek(date):
    return date - datetime.timedelta(days=(date.isoweekday() % 7) - 1)


def formeThreeWeekRange(date):
    result = dict()
    for i in [-1, 1]:
        dt_prev = startDayOfWeek(date + datetime.timedelta(7 * i))
        result[dt_prev] = dt_prev.strftime("%d %m") + " - " + (dt_prev + datetime.timedelta(6)).strftime("%d %m")
    return result


def weekRangeStr(date):
    return date.strftime("%d %m") + " - " + (date + datetime.timedelta(6)).strftime("%d %m")
