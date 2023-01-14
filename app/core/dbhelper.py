import sqlite3 as sq

from app.data.keyspace import DatabaseColumnsUser
from app.core.googleanalytics import analytic_wrapper_with_id, KeyParams

global database, cursor


async def db_connect(name):
    global database, cursor
    database = sq.connect(name)
    cursor = database.cursor()


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
        can_save = await can_save_group(id_user)
        if not can_save:
            return
        cursor.execute(f"INSERT INTO users_groups (id_user, saved_group_id, saved_group_name) "
                       f"VALUES ({id_user}, {group_id}, '{group_name}')")
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
        can_save = await can_save_teacher(id_user)
        if not can_save:
            return
        cursor.execute(f"INSERT INTO users_teachers (id_user, saved_teacher_id, saved_teacher_name) "
                       f"VALUES ({id_user}, {teacher_id}, '{teacher_name}')")
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


# REMOVE

async def remove_group_for_user(id_user: int, group_id: int, group_name: str):
    global database, cursor
    try:
        cursor.execute(f"DELETE FROM users_groups WHERE id_user = {id_user}"
                       f" AND saved_group_id = {group_id}"
                       f" AND saved_group_name = '{group_name}'")
        database.commit()
    except Exception as e:
        pass


async def remove_teacher_for_user(id_user: int, teacher_id: int, teacher_name: str):
    global database, cursor
    try:
        cursor.execute(f"DELETE FROM users_teachers WHERE id_user = {id_user}"
                       f" AND saved_teacher_id = {teacher_id}"
                       f" AND saved_teacher_name = '{teacher_name}'")
        database.commit()
    except Exception as e:
        pass


# GET

async def get_all_from_user(id_user: int) -> dict:
    res = cursor.execute(f"SELECT * FROM users WHERE id_user = {id_user}").fetchone()
    if res is None:
        return dict()
    data = dict()
    data[DatabaseColumnsUser.LAST_GROUP] = res[1]
    data[DatabaseColumnsUser.LAST_GROUP_NAME] = res[2]

    data[DatabaseColumnsUser.LAST_TEACHER] = res[3]
    data[DatabaseColumnsUser.LAST_TEACHER_NAME] = res[4]

    data[DatabaseColumnsUser.CODE_AUD] = res[5]
    data[DatabaseColumnsUser.CODE_BUILDING] = res[6]

    return data


async def get_from_user(id_user: int, column):
    res = cursor.execute(f"SELECT {column} FROM users WHERE id_user = {id_user}").fetchone()
    return res[0] if res is not None else None


async def get_saved_groups(id_user: int):
    res = cursor.execute(
        f"SELECT saved_group_id, saved_group_name FROM users_groups WHERE id_user = {id_user}").fetchall()
    return res if res is not None else list()


async def get_saved_teachers(id_user: int):
    res = cursor.execute(
        f"SELECT saved_teacher_id, saved_teacher_name FROM users_teachers WHERE id_user = {id_user}").fetchall()
    return res if res is not None else list()


async def can_save_group(id_user: int) -> bool:
    current_count = await get_current_groups_count(id_user)
    max_count = await get_max_groups_count()
    return current_count < max_count


async def can_save_teacher(id_user: int) -> bool:
    current_count = await get_current_teachers_count(id_user)
    max_count = await get_max_teachers_count()
    return current_count < max_count


async def get_max_groups_count() -> int:
    res = cursor.execute(
        f"SELECT parameter FROM bot_parameters where name = 'max_groups_count'").fetchone()
    return int(res[0]) if res is not None else 0


async def get_max_teachers_count() -> int:
    res = cursor.execute(
        f"SELECT parameter FROM bot_parameters where name = 'max_teachers_count'").fetchone()
    return int(res[0]) if res is not None else 0


async def get_current_groups_count(id_user: int) -> int:
    res = cursor.execute(
        f"SELECT COUNT(*) FROM users_groups where id_user = {id_user}").fetchone()
    return int(res[0]) if res is not None else 0


async def get_current_teachers_count(id_user: int) -> int:
    res = cursor.execute(
        f"SELECT COUNT(*) FROM users_teachers where id_user = {id_user}").fetchone()
    return int(res[0]) if res is not None else 0
