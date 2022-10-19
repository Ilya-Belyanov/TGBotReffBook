class EdForm:
    COMMON = 'common'
    DISTANT = 'distant'
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
