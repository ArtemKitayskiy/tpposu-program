import sqlite3
from datetime import datetime
import numpy as np
db_name = "database.db"


def add_data_in_table(data, user_id, exp_date, comment):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""INSERT INTO exp_info (
        user_id, exp_date, comment)
        VALUES (
        '{user_id}',
        '{exp_date}',
        '{comment}'
        )"""
    cur.execute(command)
    con.commit()

    command = f"""SELECT MAX(id) FROM exp_info"""
    cur.execute(command)
    ex_id = cur.fetchall()
    ex_id = ex_id[0][0]

    print('saving started')
    start_time = datetime.now()
    data = np.column_stack(([ex_id] * len(data),data))
    cur.executemany("INSERT INTO exp_logs (exp_id, cad_num, ch_1, ch_2, ch_3, ch_4, ch6_disp, ch6_mean, ch_14, ch_44, ch_54, ch_65, ch_7, ch_74) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
    con.commit()
    cur.close()
    print('saving finished:', datetime.now() - start_time)


def get_data_from_table(exp_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT 
        cad_num, ch_1, ch_2, ch_3,
        ch_4, ch6_mean, ch6_disp,
        ch_14, ch_44, ch_54, ch_65, ch_7, ch_74
        FROM exp_logs WHERE exp_id == '{exp_id}'"""
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    return result


def sortData(exp_id, field, order, filter_condition):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT 
        cad_num, ch_1, ch_2, ch_3,
        ch_4, ch6_mean, ch6_disp,
        ch_14, ch_44, ch_54, ch_65, ch_7, ch_74
        FROM exp_logs WHERE exp_id == '{exp_id}' {filter_condition} ORDER BY {field} {order}"""
    print(command)
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    return result


def get_exp_data_by_id(exp_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT exp_date
            FROM exp_info WHERE user_id == '{exp_id}'"""
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    if len(result)==0:
        print('У данного пользователя нет экспериментов')
        return []
    return result


def get_exp_date(exp_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT exp_date FROM exp_info WHERE user_id == '{exp_id}'"""
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    if len(result)==0:
        print('У данного пользователя нет экспериментов')
        return []
    return result


def get_exp_comment(exp_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT comment FROM exp_info WHERE id == '{exp_id}'"""
    cur.execute(command)
    result = cur.fetchall()
    return result[0][0]


def get_exp_by_date(date):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT id FROM exp_info WHERE exp_date == '{date}'"""
    cur.execute(command)
    ex_id = cur.fetchall()[0][0]
    return get_data_from_table(ex_id)



def get_sorted_data(date, field, order, filter_condition):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    command = f"""SELECT id FROM exp_info WHERE exp_date == '{date}'"""
    cur.execute(command)
    ex_id = cur.fetchall()[0][0]
    return sortData(ex_id, field, order, filter_condition)

