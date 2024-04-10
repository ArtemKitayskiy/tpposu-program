import sqlite3
db_name = "database.db"


def add_user(login, password):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    # Проверка на логин
    try:
        command = f"""INSERT INTO users (login, password, is_active)
                           VALUES ('{login}', '{password}', 0) """
        cur.execute(command)
        con.commit()
        cur.close()
        response = 'Регистрация прошла успешно'
    except:
        response = 'Пользователь сущестсвует'
        cur.close()
    return response


def check_signed_users():
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT login FROM users WHERE is_active == 1 """
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    if result:
        return result[0][0]
    else:
        return False


def set_user_active_status(login):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT login FROM users WHERE is_active == 1 """
    cur.execute(command)
    result = cur.fetchall()
    command = f"""UPDATE users SET is_active=0 WHERE login == '{result[0][0]}'"""
    cur.execute(command)
    con.commit()
    command = f"""UPDATE users SET is_active=1 WHERE login == '{login}'"""
    cur.execute(command)
    con.commit()
    cur.close()


def get_userid_by_login(login):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT user_id FROM users WHERE login == '{login}' """
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    if result:
        return result[0][0]
    else:
        return 'Пользователь не найден'


def get_exps_by_user_id(user_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT id FROM exp_info WHERE user_id == '{user_id}' """
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    return result


def check_user_password(login, password):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT password FROM users WHERE login == '{login}' """
    cur.execute(command)
    user_passwd = cur.fetchall()
    cur.close()
    if user_passwd[0][0] == password:
        return True
    else:
        return False


def get_users_logins():
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT login FROM users"""
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    return result



