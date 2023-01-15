CREATE TABLE IF NOT EXISTS users(id_user INT UNIQUE PRIMARY KEY,
                   saved_group_id INT DEFAULT NULL, saved_group_name TEXT DEFAULT NULL,
                   saved_teacher_id INT DEFAULT NULL, saved_teacher_name TEXT DEFAULT NULL,
                   last_group_id INT DEFAULT NULL, last_group_name TEXT DEFAULT NULL,
                   last_teacher_id INT DEFAULT NULL, last_teacher_name TEXT DEFAULT NULL,
                   code_aud INT DEFAULT NULL, code_building INT DEFAULT NULL,
                   active NUMERIC DEFAULT 1);

CREATE TABLE IF NOT EXISTS admins(id_user INT UNIQUE);


-- Создаем новую таблицу с сохраненными группами
CREATE TABLE IF NOT EXISTS users_groups(id_user INTEGER,
                                        saved_group_id INT,
                                        saved_group_name TEXT,
                                        FOREIGN KEY(id_user) REFERENCES users(id_user)  ON DELETE CASCADE);

-- Создаем новую таблицу с сохраненными преподавателями
CREATE TABLE IF NOT EXISTS users_teachers(id_user INTEGER,
                                        saved_teacher_id INT,
                                        saved_teacher_name TEXT,
                                        FOREIGN KEY(id_user) REFERENCES users(id_user)  ON DELETE CASCADE);

-- Создаем новую таблицу с системными параметрами
CREATE TABLE IF NOT EXISTS bot_parameters(name TEXT,
                                         parameter TEXT);

INSERT into bot_parameters values ('max_groups_count', '5'), ('max_teachers_count', '5');