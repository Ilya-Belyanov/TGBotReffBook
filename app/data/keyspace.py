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
    TYPE = "type"
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
    TEACHER = "teacher"
    PLACE = "place"

    SAVE_GROUP = "save"
    SAVE_TEACHER = "sv_thr"

    REMOVE_GROUP = "remove_group"
    REMOVE_TEACHER = "remove_teacher"

    DATES = "dates"


class Separators:
    KEY_DATA = ":"
    DATA_META = "|"


class StateKeyWords:
    INSTITUTE = "institute"
    ED_FORM = 'ed_form'
    ED_DEGREE = 'ed_degree'
    LEVEL = "level"


class DatabaseColumnsUser:
    LAST_GROUP = "last_group_id"
    LAST_GROUP_NAME = "last_group_name"

    LAST_TEACHER = "last_teacher_id"
    LAST_TEACHER_NAME = "last_teacher_name"

    CODE_AUD = "code_aud"
    CODE_BUILDING = "code_building"

    ACTIVE = "active"


class DatabaseColumnUserGroups:
    ID_USER = "id_user"
    SAVED_GROUP = "saved_group_id"
    SAVED_GROUP_NAME = "saved_group_name"


class DatabaseColumnUserTeachers:
    ID_USER = "id_user"
    SAVED_TEACHER = "saved_teacher_id"
    SAVED_TEACHER_NAME = "saved_teacher_name"


EDUCATION_FORMS_RU = {EdForm.COMMON: "Очная", EdForm.EVENING: "Очно-заочная", EdForm.DISTANT: "Заочная"}
EDUCATION_DEGREE_RU = {EdDegree.BACHELOR: "Бакалавр", EdDegree.MAGISTRACY: "Магистр",
                       EdDegree.SPECIALIST: "Специалист",  EdDegree.GRADUATE_STUDENT: "Аспирант",
                       EdDegree.SPO: "СПО"}
