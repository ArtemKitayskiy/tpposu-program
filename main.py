import sys
import tkinter as tk
from get_data import *
from tkinter import messagebox, ttk
from bdUtils import addDataToDB, signAndLog

def out_table(window_name, data):

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
    errs = data['errors']
    data = data['result']

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

    def out_data():
        count = int(frames_entry.get())
        data = {'result':[],'errors':[]}
        for i in range(0,count):
            data['result'].append([i+1]+get_data()['result'])
            data['errors'].append([i+1]+get_data()['errors'])
        out_table(new_registration_window, data)

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
    new_data_management_window = tk.Toplevel(root)
    new_data_management_window.title("Окно управления данными")
    new_data_management_window.geometry("400x200")
    center_window(new_data_management_window)


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