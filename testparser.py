from scheduleparser import ScheduleParser
from data import *

if __name__ == "__main__":
    print(ScheduleParser.getCourses(94, EdForm.COMMON, EdDegree.MAGISTRACY))
    print(ScheduleParser.getGroupsByParameters(94, EdForm.COMMON, EdDegree.MAGISTRACY, 1))
