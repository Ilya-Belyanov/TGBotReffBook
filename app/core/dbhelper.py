import sqlite3 as sq

from app.data.keyspace import DatabaseColumnsUser
from app.core.googleanalytics import analytic_wrapper_with_id, KeyParams

global database, cursor


async def db_connect(name):
    global database, cursor
    database = sq.connect(name)
    cursor = database.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id_user INT UNIQUE,"
                   "saved_group_id INT DEFAULT NULL, saved_group_name TEXT DEFAULT NULL,"
                   "saved_teacher_id INT DEFAULT NULL, saved_teacher_name TEXT DEFAULT NULL,"
                   "last_group_id INT DEFAULT NULL, last_group_name TEXT DEFAULT NULL,"
                   "last_teacher_id INT DEFAULT NULL, last_teacher_name TEXT DEFAULT NULL,"
                   "code_aud INT DEFAULT NULL, code_building INT DEFAULT NULL,"
                   "active NUMERIC DEFAULT 1)")

    cursor.execute("CREATE TABLE IF NOT EXISTS admins(id_user INT UNIQUE)")

    database.commit()


@analytic_wrapper_with_id("New_user_id", True)
async def add_user(id_user: int) -> bool:
    global database, cursor
    res = cursor.execute(f"SELECT id_user FROM users WHERE id_user = {id_user}").fetchone()
    if res is not None:
        return False
    cursor.execute(f"INSERT INTO users (id_user) VALUES ({id_user})")
    database.commit()
    return True


async def is_admin(id_user: int) -> bool:
    global database, cursor
    res = cursor.execute(f"SELECT id_user FROM admins WHERE id_user = {id_user}").fetchone()
    return res is not None


async def user_count() -> int:
    global database, cursor
    res = cursor.execute(f"SELECT COUNT(id_user) FROM users").fetchone()
    return res[0]


async def all_users() -> list:
    global database, cursor
    res = cursor.execute(f"SELECT id_user FROM users").fetchall()
    return res


# SAVE
async def save_group_for_user(id_user: int, group_id: int, group_name: str):
    global database, cursor
    try:
        cursor.execute(f"UPDATE users SET saved_group_id = {group_id}, saved_group_name = '{group_name}'"
                       f" WHERE id_user = {id_user}")
        database.commit()
    except Exception as e:
        pass


async def update_last_group_for_user(id_user: int, group_id: int, group_name: str):
    global database, cursor
    try:
        cursor.execute(f"UPDATE users SET last_group_id = {group_id}, last_group_name = '{group_name}'"
                       f" WHERE id_user = {id_user}")
        database.commit()
    except Exception as e:
        pass


async def save_teacher_for_user(id_user: int, teacher_id: int, teacher_name: str):
    global database, cursor
    try:
        cursor.execute(f"UPDATE users SET saved_teacher_id = {teacher_id}, saved_teacher_name = '{teacher_name}'"
                       f" WHERE id_user = {id_user}")
        database.commit()
    except Exception as e:
        pass


async def update_last_teacher_for_user(id_user: int, teacher_id: int, teacher_name: str):
    global database, cursor
    try:
        cursor.execute(f"UPDATE users SET last_teacher_id = {teacher_id}, last_teacher_name = '{teacher_name}'"
                       f" WHERE id_user = {id_user}")
        database.commit()
    except Exception as e:
        pass


async def save_str_for_user(id_user: int, column: str, value: str):
    global database, cursor
    try:
        cursor.execute(f"UPDATE users SET {column} = '{value}' WHERE id_user = {id_user}")
        database.commit()
    except Exception as e:
        pass


async def save_int_for_user(id_user: int, column: str, value: int):
    global database, cursor
    try:
        cursor.execute(f"UPDATE users SET {column} = {value} WHERE id_user = {id_user}")
        database.commit()
    except Exception as e:
        pass

# GET
async def get_all_from_user(id_user: int) -> dict:
    res = cursor.execute(f"SELECT * FROM users WHERE id_user = {id_user}").fetchone()
    if res is None:
        return dict()
    data = dict()
    data[DatabaseColumnsUser.SAVED_GROUP] = res[1]
    data[DatabaseColumnsUser.SAVED_GROUP_NAME] = res[2]
    data[DatabaseColumnsUser.SAVED_TEACHER] = res[3]
    data[DatabaseColumnsUser.SAVED_TEACHER_NAME] = res[4]

    data[DatabaseColumnsUser.LAST_GROUP] = res[5]
    data[DatabaseColumnsUser.LAST_GROUP_NAME] = res[6]
    data[DatabaseColumnsUser.LAST_TEACHER] = res[7]
    data[DatabaseColumnsUser.LAST_TEACHER_NAME] = res[8]

    data[DatabaseColumnsUser.CODE_AUD] = res[9]
    data[DatabaseColumnsUser.CODE_BUILDING] = res[10]
    return data


async def get_from_user(id_user: int, column):
    res = cursor.execute(f"SELECT {column} FROM users WHERE id_user = {id_user}").fetchone()
    if res is None:
        return None
    return res[0]
