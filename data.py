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


EDUCATION_FORMS_RU = {EdForm.COMMON: "Очная", EdForm.EVENING: "Очно-заочная", EdForm.DISTANT: "Заочная"}
EDUCATION_DEGREE_RU = {EdDegree.BACHELOR: "Бакалавр", EdDegree.MAGISTRACY: "Магистр",
                       EdDegree.SPECIALIST: "Специалист",  EdDegree.GRADUATE_STUDENT: "Аспирант",
                       EdDegree.SPO: "СПО"}
