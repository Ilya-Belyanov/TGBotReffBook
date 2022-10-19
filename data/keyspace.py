class EdForm:
    COMMON = 'common'
    DISTANT = 'distance'
    EVENING = 'evening'


class EdDegree:
    BACHELOR = 0
    MAGISTRACY = 1
    SPECIALIST = 2
    GRADUATE_STUDENT = 3
    SPO = 4


class LessonsKeyWords:
    DAY = "day"
    LESSONS = "lessons"
    START_TIME = "start_time"
    END_TIME = "end_time"
    NAME = "name"
    GROUPS_NAME = "groups_name"
    GROUPS_LINK = "groups_link"
    TEACHER_NAME = "teacher_name"
    TEACHER_LINK = "teacher_link"
    PLACE_NAME = "place_name"
    PLACE_LINK = "place_link"
    RESOURCE_NAME = "resource_name"
    RESOURCE_LINK = "resource_link"


class IdCommandKeyWords:
    INSTITUTE = "inst"
    ED_FORM = "ed_form"
    ED_DEGREE = "ed_degree"
    LEVEL = "level"
    GROUP = "group"
    DATES = "dates"


class Separators:
    KEY_DATA = ":"
    DATA_META = "|"


class StateKeyWords:
    INSTITUTE = "institute"
    ED_FORM = 'ed_form'
    ED_DEGREE = 'ed_degree'
    LEVEL = "level"
    GROUP = "group"
    GROUP_NAME = "group_name"


EDUCATION_FORMS_RU = {EdForm.COMMON: "Очная", EdForm.EVENING: "Очно-заочная", EdForm.DISTANT: "Заочная"}
EDUCATION_DEGREE_RU = {EdDegree.BACHELOR: "Бакалавр", EdDegree.MAGISTRACY: "Магистр",
                       EdDegree.SPECIALIST: "Специалист",  EdDegree.GRADUATE_STUDENT: "Аспирант",
                       EdDegree.SPO: "СПО"}
