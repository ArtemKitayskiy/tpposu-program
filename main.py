import sys
import tkinter as tk
import datetime
from get_data import *
from tkinter import messagebox, ttk
from bdUtils import addDataToDB, signAndLog


global user_login
user_login = ""


def out_table(window_name, data=None):

    # Создаем Treeview
    columns = tuple(conf.keys())
    tree = ttk.Treeview(window_name, show="headings", columns=columns)
    for column in columns:
        tree.heading(f'{column}', text=column)
    # Устанавливаем заголовки
    # tree.heading('ID', text='ID')
    # tree.heading('Имя', text='Имя')
    # tree.heading('Возраст', text='Возраст')
    # tree.heading('Город', text='Город')
    if data:
        errs = data['errors']
        data = data['result']
    else:
        data = []

    for row in data:
        tree.insert('', tk.END, values=row)

    # Установим автоматическое масштабирование ширины колонок
    for column in tree['columns']:
        tree.column(column, width = 70,stretch=True)


    # Упаковываем Treeview
    tree.pack(expand=True, fill='both')


def on_key_press(event):
    if event.keysym == 'Return':
        button_login.invoke()

def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_width = window.winfo_width()
    window_height = window.winfo_height()

    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2

    window.geometry(f"+{x_coordinate}+{y_coordinate}")

def registration_window():
    registration_window = tk.Toplevel(root)
    registration_window.title("Окно регистрации")
    registration_window.geometry("400x200")
    center_window(registration_window)
    registration_window.resizable(False, False)

    label_username = tk.Label(registration_window, text="Логин:")
    label_username.grid(row=0, column=0, sticky=tk.E)
    label_username.place(x=100, y=50)

    reg_user = tk.Entry(registration_window)
    reg_user.grid(row=0, column=1)
    reg_user.place(x=150, y=50)

    label_password = tk.Label(registration_window, text="Пароль:")
    label_password.grid(row=1, column=0, sticky=tk.E)
    label_password.place(x=100, y=80)

    reg_password = tk.Entry(registration_window, show="*")
    reg_password.grid(row=1, column=1)
    reg_password.place(x=150, y=80)


    def add_user():
        username = reg_user.get()
        password = reg_password.get()
        messagebox.showinfo('Информация о регистрации',signAndLog.add_user(username, password))
        registration_window.destroy()

    button_login = tk.Button(registration_window, text="Регистрация", command=add_user, width=10, height=2)
    button_login.grid(row=2, columnspan=2)
    button_login.place(x=150, y=110)
    

def check_credentials():
    username = entry_username.get()
    password = entry_password.get()
    result = signAndLog.check_user_password(username,password)

    if result[0] == True:
        messagebox.showinfo("Успешная авторизация", "Вы успешно авторизованы!")
        signAndLog.set_user_active_status(username)
        user_login = username
        root.withdraw()
        open_main_window()
    else:
        messagebox.showerror("Ошибка авторизации", result[1])
    

def open_main_window():
    main_window = tk.Toplevel(root)
    main_window.title("Главное окно")
    main_window.geometry("400x200")
    main_window.resizable(False, False)
    center_window(main_window)

    # Создаем словарь, где ключами являются названия кнопок, а значениями - функции для открытия соответствующих окон
    buttons_actions = {
        "Регистрация данных": open_registration_window,
        "Проведение HTP": open_htp_window,
        "Управление данными": open_data_management_window,
        "Информация о ПО": open_software_info_window,
        "Выход": sys.exit,
    }

    # Создаем кнопки на основе элементов словаря
    for text, action in buttons_actions.items():
        button = tk.Button(main_window, text=text, command=action)
        button.pack(pady=5)


def open_registration_window():
    global data
    data = {'result':[],'errors':[]}
    def out_data():
        count = int(frames_entry.get())
        for i in range(0,count):
            data['result'].append([i+1]+get_data()['result'])
            
            errors = get_data()['errors']
            if len(data['errors'])!=0:
                messagebox.showerror("Ошибка авторизации", errors)
          
        out_table(new_registration_window, data)

        def safe_data():
            user_login = signAndLog.check_signed_users()
            print(user_login)
            user_id = signAndLog.get_userid_by_login(user_login)
            addDataToDB.add_data_in_table(data['result'], user_id, datetime.datetime.now(), comm_entry.get())


        comm_label = tk.Label(new_registration_window, text="Комментарий:")
        comm_label.pack(side=tk.LEFT, padx=5, pady=5)

        comm_entry = tk.Entry(new_registration_window)
        comm_entry.pack(side=tk.LEFT, padx=5, pady=5)

        start_button = tk.Button(new_registration_window, text="Сохранить", command=safe_data)
        start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        


    new_registration_window = tk.Toplevel(root)
    new_registration_window.title("Окно регистрации данных")
    new_registration_window.geometry("1280x720")
    center_window(new_registration_window)

    # Создание и размещение виджетов
    frames_label = tk.Label(new_registration_window, text="Число кадров:")
    frames_label.pack(side=tk.LEFT, padx=5, pady=5)

    frames_entry = tk.Entry(new_registration_window)
    frames_entry.pack(side=tk.LEFT, padx=5, pady=5)

    start_button = tk.Button(new_registration_window, text="Начать опрос", command=out_data)
    start_button.pack(side=tk.LEFT, padx=5, pady=5)

    


def open_htp_window():
    new_htp_window = tk.Toplevel(root)
    new_htp_window.title("Окно проведения HTP")
    new_htp_window.geometry("400x200")
    center_window(new_htp_window)
    


def open_data_management_window():
    selected_date = None
    new_data_management_window = tk.Toplevel(root)
    new_data_management_window.title("Окно управления данными")
    new_data_management_window.geometry("1280x720")
    center_window(new_data_management_window)

    columns = tuple(conf.keys())
    tree = ttk.Treeview(new_data_management_window, columns=columns, show="headings", height=20)

    # Устанавливаем заголовки для колонок
    for col in columns:
        tree.heading(col, text=col)
    # Установим автоматическое масштабирование ширины колонок
    for column in tree['columns']:
        tree.column(column, width = 80, stretch=True)
    # Заполните таблицу данными, если это необходимо
    # Пример добавления данных:
    # tree.insert("", "end", values=("1", "John", "30", "New York"))

    # Разместите таблицу внизу окна
    tree.grid(row=2, column=0, columnspan=10, padx=10, pady=10)

    # Добавьте прокрутку для таблицы при необходимости
    scrollbar = ttk.Scrollbar(new_data_management_window, orient="vertical", command=tree.yview)
    scrollbar.grid(row=2, column=10, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)


    def combobox_changed(event):

        def date_changed(event):
            nonlocal selected_date
            # Очистка всех элементов в Treeview
            for item in tree.get_children():
                tree.delete(item)

            selected_date = dropdown_3.get()[1:-1]
            data = addDataToDB.get_exp_by_date(selected_date)

            for row in data:
                tree.insert('', tk.END, values=row)


        selected_value = dropdown.get()

        user_id = signAndLog.get_userid_by_login(selected_value)

        dates = addDataToDB.get_exp_data_by_id(user_id)
        dropdown_frame_3 = tk.Frame(new_data_management_window)
        dropdown_frame_3.grid(row=1, column=0, padx=10, pady=10)

        label_3 = tk.Label(dropdown_frame_3, text="Дата")
        label_3.pack(side='top', anchor='w')

        dropdown_values_3 = ["Элемент X", "Элемент Y", "Элемент Z"]
        dropdown_3 = ttk.Combobox(dropdown_frame_3, values=dates, state="readonly")
        dropdown_3.pack(side='left')
        dropdown_3.bind("<<ComboboxSelected>>", date_changed)

    dropdown_frame = tk.Frame(new_data_management_window)
    dropdown_frame.grid(row=0, column=0, padx=10, pady=10)

    label = tk.Label(dropdown_frame, text="Ответственный")
    label.pack(side='top', anchor='w')

    dropdown_values = signAndLog.get_users_logins()
    dropdown = ttk.Combobox(dropdown_frame, values=dropdown_values, state='readonly')
    dropdown.pack(side='left')
    dropdown.bind("<<ComboboxSelected>>", combobox_changed)

    dropdown_frame_2 = tk.Frame(new_data_management_window)
    dropdown_frame_2.grid(row=0, column=1, padx=10, pady=10)

    label_2 = tk.Label(dropdown_frame_2, text="Столбец для сортировки")
    label_2.pack(side='top', anchor='w')

    dropdown_values_2 = ["Элемент A", "Элемент B", "Элемент C", "Элемент D"]
    dropdown_2 = ttk.Combobox(dropdown_frame_2, values=columns, state="readonly")
    dropdown_2.set(columns[0])
    dropdown_2.pack(side='left')


    dropdown_frame_4 = tk.Frame(new_data_management_window)
    dropdown_frame_4.grid(row=1, column=1, padx=10, pady=10)

    label_4 = tk.Label(dropdown_frame_4, text="Порядок сортировки")
    label_4.pack(side='top', anchor='w')

    dropdown_values_4 = ["По возрастанию", "По убыванию"]
    dropdown_4 = ttk.Combobox(dropdown_frame_4, values=dropdown_values_4, state="readonly")
    dropdown_4.set("По возрастанию")
    dropdown_4.pack(side='left')

    dropdown_frame_5 = tk.Frame(new_data_management_window)
    dropdown_frame_5.grid(row=0, column=2, padx=10, pady=10)

    label_5 = tk.Label(dropdown_frame_5, text="Канал")
    label_5.pack(side='top', anchor='w')

    dropdown_values_5 = ["Элемент Q", "Элемент R", "Элемент S"]
    dropdown_5 = ttk.Combobox(dropdown_frame_5, values=columns, state="readonly")
    dropdown_5.set(columns[0])
    dropdown_5.pack(side='left')

    min_entry_frame = tk.Frame(new_data_management_window)
    min_entry_frame.grid(row=1, column=2, padx=10, pady=10)

    label_6 = tk.Label(min_entry_frame, text="Минимальное")
    label_6.pack(side='top', anchor='w')

    entry_1 = tk.Entry(min_entry_frame)
    entry_1.pack(side='top')

    man_entry_frame = tk.Frame(new_data_management_window)
    man_entry_frame.grid(row=1, column=3, padx=10, pady=10)

    label_7 = tk.Label(man_entry_frame, text="Максимальное")
    label_7.pack(side='top', anchor='w')

    entry_2 = tk.Entry(man_entry_frame)
    entry_2.pack(side='top')

    def get_filtered_data(col, sort_type, min, max):
        for item in tree.get_children():
            tree.delete(item)
        sort_type = 'DESC' if sort_type == 'По убыванию' else ''

        if min!='' and max!='':
            filter_condition = f'AND {conf[col]} BETWEEN {min} AND {max}'
        elif min!='':
            filter_condition = f'AND {conf[col]} >= {min}'
        elif max!='':
            filter_condition = f'AND {conf[col]} <= {max}'
        else:
            filter_condition = ''
        
        data = addDataToDB.get_sorted_data(selected_date, conf[col], sort_type, filter_condition)

        for row in data:
                tree.insert('', tk.END, values=row)

    button = tk.Button(new_data_management_window, text="Установить фильтр", width=20, height=3, command= lambda: get_filtered_data(dropdown_5.get(), dropdown_4.get(), entry_1.get(), entry_2.get()))
    button.grid(row=0, column=4, padx=10, pady=10, rowspan=2)

    



def open_software_info_window():
    new_software_info_window = tk.Toplevel(root)
    new_software_info_window.title("Окно информации о ПО")
    new_software_info_window.geometry("400x200")
    center_window(new_software_info_window)
    label = tk.Label(new_software_info_window, text="Текст")
    label.pack()


root = tk.Tk()
root.title("Окно авторизации")
root.geometry("400x200")
root.resizable(False, False)
center_window(root)

# Создание и размещение виджетов
label_username = tk.Label(root, text="Логин:")
label_username.grid(row=0, column=0, sticky=tk.E)
label_username.place(x=100, y=50)

entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1)
entry_username.place(x=150, y=50)

label_password = tk.Label(root, text="Пароль:")
label_password.grid(row=1, column=0, sticky=tk.E)
label_password.place(x=100, y=80)

entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1)
entry_password.place(x=150, y=80)

button_login = tk.Button(root, text="Ввод", command=check_credentials, width=10, height=2)
button_login.grid(row=2, columnspan=2)
button_login.place(x=150, y=110)

button_registraion = tk.Button(root, text="Регистрация", command=registration_window, width=10, height=2)
button_registraion.grid(row=2, columnspan=2)
button_registraion.place(x=150, y=150)


root.bind("<Return>", on_key_press)
# Запуск главного цикла обработки событий
root.mainloop()