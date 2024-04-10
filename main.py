import tkinter as tk
from tkinter import messagebox


def check_credentials():
    username = entry_username.get()
    password = entry_password.get()

    if username in ["Наников", "Китайский", "Викторов"] and password == "password":
        messagebox.showinfo("Успешная авторизация", "Вы успешно авторизованы!")
        open_main_window()
    else:
        messagebox.showerror("Ошибка авторизации", "Неверный логин или пароль")


def open_main_window():
    main_window = tk.Toplevel(root)
    main_window.title("Главное окно")
    main_window.geometry("400x200")

    # Создаем словарь, где ключами являются названия кнопок, а значениями - функции для открытия соответствующих окон
    buttons_actions = {
        "Регистрация данных": open_registration_window,
        "Проведение HTP": open_htp_window,
        "Управление данными": open_data_management_window,
        "Информация о ПО": open_software_info_window
    }

    # Создаем кнопки на основе элементов словаря
    for text, action in buttons_actions.items():
        button = tk.Button(main_window, text=text, command=action)
        button.pack(pady=5)


def open_registration_window():
    new_registration_window = tk.Toplevel(root)
    new_registration_window.title("Окно регистрации данных")
    new_registration_window.geometry("400x200")


def open_htp_window():
    new_htp_window = tk.Toplevel(root)
    new_htp_window.title("Окно проведения HTP")
    new_htp_window.geometry("400x200")


def open_data_management_window():
    new_data_management_window = tk.Toplevel(root)
    new_data_management_window.title("Окно управления данными")
    new_data_management_window.geometry("400x200")


def open_software_info_window():
    new_software_info_window = tk.Toplevel(root)
    new_software_info_window.title("Окно информации о ПО")
    new_software_info_window.geometry("400x200")
    label = tk.Label(new_software_info_window, text="Текст")
    label.pack()


root = tk.Tk()
root.title("Окно авторизации")
root.geometry("400x200")

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

# Запуск главного цикла обработки событий
root.mainloop()