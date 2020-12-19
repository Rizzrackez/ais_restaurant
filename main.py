import sys
import string
import random

import tkinter as tk
import ctypes
from main_services import *
from database_services import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from tkinter import ttk
from tkinter import font as tkFont

# ????????
from tkinter.ttk import *

super_master = None

TIME_RESERVATION = ['9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
                    '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
                    '20:00', '20:30', '21:00']

PERMISSION_LIST = ['Администратор', 'Метрдотель']


class LoginWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.employee_id = None
        self.master.minsize(300, 230)
        self.master.maxsize(300, 230)
        self.create_widgets()

    def create_widgets(self):

        def on_entry_click(event):
            """function that gets called whenever entry is clicked"""
            if self.username_entry.get() == '8900553535':
                self.username_entry.delete(0, "end")  # delete all the text in the entry
                self.username_entry.insert(0, '')  # Insert blank for user input
                self.username_entry.config(fg='black')

        def on_focusout(event):
            if self.username_entry.get() == '':
                self.username_entry.insert(0, '8900553535')
                self.username_entry.config(fg='grey')

        self.auth_label = tk.Label(self.master, text='Ресторан "Аврора"')
        self.auth_label.pack(pady=(20, 10))

        self.username_label = tk.Label(self.master, text="Телефон*")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.username_entry.pack(pady=(0, 15))

        self.username_entry.insert(0, '8900553535')
        self.username_entry.bind('<FocusIn>', on_entry_click)
        self.username_entry.bind('<FocusOut>', on_focusout)
        self.username_entry.config(fg='grey')

        self.password_label = tk.Label(self.master, text="Токен аутентификации*")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.master, textvariable=tk.StringVar(), show='*')
        self.password_entry.pack(pady=(0, 10))

        self.auth_button_style = ttk.Style()
        self.auth_button_style.configure('my.TButton', font=('Helvetica', 10))
        self.login_button = ttk.Button(self.master, text="Войти", style='my.TButton', command=self.login_verification)
        self.login_button.pack()

        self.username_label.config(font=("large", 11))
        self.password_label.config(font=("large", 11))
        self.auth_label.config(font=("large", 14))

        self.username_entry.config(font=("large", 11))
        self.password_entry.config(font=("large", 11))

    def login_verification(self):
        untested_employee_id = login_verification_in_db(self.username_entry.get(), self.password_entry.get())
        if untested_employee_id is not None:
            if untested_employee_id[1] == 'worker':
                self.employee_id = untested_employee_id[0]
                self.create_info_admin_table_window(MainWindow)

            elif untested_employee_id[1] == 'admin':
                self.employee_id = untested_employee_id[0]
                self.create_info_admin_table_window(AdminPanel)

        else:
            messagebox.showwarning(title='Error', message='Неверный телефон или токен авторизации!')

    def create_info_admin_table_window(self, _class):
        self.master.withdraw()
        calendar_window = tk.Toplevel(self.master)
        _class(calendar_window, self.employee_id)


class AdminPanel:
    def __init__(self, master=None, employee_id=None):
        self.master = master
        self.employee_id = employee_id
        self.master.geometry(centering_window(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.master.minsize(500, 330)
        self.master.maxsize(500, 330)
        self.master.title("Панель администратора")
        self.master.iconbitmap('media/admin.ico')
        global admin_master
        admin_master = self.master
        self.create_widgets()

    def create_widgets(self):
        self.auth_label = tk.Label(self.master, text="Панель администратора")
        self.auth_label.pack()
        self.auth_label.config(font=("large", 20), pady=20)

        self.add_employee_button = ttk.Button(self.master, text="Добавить сотрудника",
                                              command=lambda: self.create_employee_window(EmployeeWindow))
        self.add_employee_button.pack(pady=5)

        self.get_list_employees_button = ttk.Button(self.master, text="Просмотр всех сотрудников",
                                              command=lambda: self.get_list_employees(EmployeesListWindow))
        self.get_list_employees_button.pack(pady=5)

        self.get_reservation_info = ttk.Button(self.master, text="Просмотр бронирования за конкретную дату",
                                              command=lambda: self.reservation_info_window(ReservationInfo))
        self.get_reservation_info.pack(pady=5)

        self.get_reservation_info = ttk.Button(self.master, text="Информация о всех бронированиях",
                                              command=lambda: self.reservation_table_info_window(ReservationTableInfo))
        self.get_reservation_info.pack(pady=5)

        exit_program_button_style = ttk.Style()
        exit_program_button_style.configure('myExit.TButton', font=('Helvetica', 12), background='red')
        self.exit_button = ttk.Button(self.master, style='myExit.TButton', text="Выход", command=self.exit_program)
        self.exit_button.pack()

    def exit_program(self):
        sys.exit()

    def create_employee_window(self, _class):
        calendar_window = tk.Toplevel(self.master)
        _class(calendar_window)

    def get_list_employees(self, _class):
        employees_window = tk.Toplevel(self.master)
        _class(employees_window)

    def reservation_info_window(self, _class):
        employees_window = tk.Toplevel(self.master)
        _class(employees_window)

    def reservation_table_info_window(self, _class):
        employees_window = tk.Toplevel(self.master)
        _class(employees_window)


class ReservationTableInfo:
    def __init__(self, master=None, table_number=None, date_res=None, employee=None):
        self.table_number = table_number
        self.date_res = date_res
        self.employee = employee

        self.master = master
        self.master.minsize(650, 530)
        self.master.maxsize(650, 530)
        self.master.title("Список всех бронирований")
        self.master.iconbitmap('media/admin.ico')
        self.master.geometry(centering_window(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.master.bind("<Control-f>", lambda event: self.create_filter_window(FilterReservationTableInfo))
        self.master.bind("<Control-F>", lambda event: self.create_filter_window(FilterReservationTableInfo))
        global reservation_master
        reservation_master = self.master
        self.create_widgets()

    def create_widgets(self):
        id_row = 0
        reservation_list = get_reservations_from_db(table_number=self.table_number, date_res=self.date_res,
                                                    employee=self.employee)

        if reservation_list == []:
            self.auth_label = tk.Label(self.master, text="По данным параметрам никаких данных нет!")
            self.auth_label.grid(row=id_row, column=0)
            self.auth_label.config(font=("large", 20), pady=20)

            exit_program_button_style = ttk.Style()
            exit_program_button_style.configure('myExit.TButton', font=('Helvetica', 12), background='red')
            self.exit_button = ttk.Button(self.master, style='myExit.TButton', text="Выход",
                                          command=self.destroy_table_window)
            self.exit_button.grid(row=id_row + 1, column=0, sticky="e", pady=(0, 20), padx=(0, 20))

        else:
            main_frame = Frame(self.master)
            main_frame.pack(fill=tk.BOTH, expand=1)

            my_canvas = tk.Canvas(main_frame)
            my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

            my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
            my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

            second_frame = Frame(my_canvas)

            my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

            reservation_list = get_reservations_from_db(table_number=self.table_number, date_res=self.date_res, employee=self.employee)

            id_row = 0
            for res in reservation_list:

                l1 = tk.Label(second_frame, text=f'Дата: {res["date_res"]}; Время: {res["time_res"]}; Номер столика: {res["table_number"]};\n'
                                                f'Имя клиента: {res["client_name"]}; Фамилия клиента: {res["client_surname"]}; Телефон клиента: {res["client_phone"]}\n'
                                                f'Кол-во клиентов: {res["clients_number"]}; ID метрдотеля: {res["employee"]}\n\n\n')
                l1.grid(row=id_row, column=0)
                id_row += 1

                l1.config(font=("Helvetica", 12))

            exit_program_button_style = ttk.Style()
            exit_program_button_style.configure('myExit.TButton', font=('Helvetica', 12), background='red')
            self.exit_button = ttk.Button(second_frame, style='myExit.TButton', text="Выход", command=self.destroy_table_window)
            self.exit_button.grid(row=id_row+1, column=0,  sticky="e", pady=(0, 20), padx=(0, 20))
            exit_program_button_style = ttk.Style()

        id_row = 0

    def create_filter_window(self, _class):
        # self.master.withdraw()
        filter_window = tk.Toplevel(self.master)
        _class(filter_window)

    def destroy_table_window(self):
        self.master.destroy()


class FilterReservationTableInfo:
    def __init__(self, master=None):
        self.master = master
        self.master.minsize(300, 100)
        self.master.maxsize(300, 100)
        self.master.title("Фильтр")
        self.master.iconbitmap('media/admin.ico')
        self.master.geometry(centering_window(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.create_widgets()

    def create_widgets(self):
        self.table_number_label = tk.Label(self.master, text="Номер столика:")
        self.table_number_label.grid(row=0, column=0)
        self.table_number_label.config(font=("Constantia", 12))

        self.date_res_label = tk.Label(self.master, text="Дата бронирования:")
        self.date_res_label.grid(row=1, column=0)
        self.date_res_label.config(font=("Constantia", 12))

        self.employee_label = tk.Label(self.master, text="ID сотрудника:")
        self.employee_label.grid(row=2, column=0)
        self.employee_label.config(font=("Constantia", 12))

        self.table_number_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.table_number_entry.grid(row=0, column=1)
        self.table_number_entry.config(font=("Helvetica", 12))

        self.date_res_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.date_res_entry.grid(row=1, column=1)
        self.date_res_entry.config(font=("Helvetica", 12))

        self.employee_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.employee_entry.grid(row=2, column=1)
        self.employee_entry.config(font=("Helvetica", 12))

        self.send_button = ttk.Button(self.master, text="Отправить", command= lambda: self.send_info(ReservationTableInfo))
        self.send_button.grid(row=3, column=1)

    def send_info(self, _class):
        if not check_valid_date_for_reservation(self.date_res_entry.get()):
            messagebox.showwarning(title='Error',
                                   message='Введена некоректная дата!')
            return 1
        reservation_master.withdraw()
        reservation_table_window = tk.Toplevel(admin_master)
        _class(master=reservation_table_window, table_number=self.table_number_entry.get(), date_res=self.date_res_entry.get(), employee=self.employee_entry.get())
        self.master.destroy()


class ReservationInfo:
    def __init__(self, master=None, table_number=None):
        self.master = master
        self.master.geometry(centering_window(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.master.minsize(360, 200)
        self.master.maxsize(360, 200)
        self.master.title("Информация по столикам")
        self.master.iconbitmap('media/admin.ico')

        # self.master.geometry('600x400+200+100')
        # self.master.maxsize(width=420, height=300)  # fixed window size
        # self.master.minsize(width=420, height=300)

        self.date_reservation_entry = None

        self.master.title(f"Информация по столикам")
        self.master.iconbitmap('media/res_table.ico')

        self.create_widgets()

    def create_widgets(self):
        table = tk.Label(self.master, text=f'Информация по столикам')
        table.grid(row=0, column=0, pady=(15, 20), columnspan=3)
        table.config(font=("large", 20))

        self.table_number_label = tk.Label(self.master, text="Номер столика:")
        self.date_reservation_label = tk.Label(self.master, text="Дата:")

        self.table_number_label.grid(row=1, column=0, padx=(20, 0), sticky="w")
        self.date_reservation_label.grid(row=2, column=0, padx=(20, 0), sticky="w")

        self.date_reservation_label.config(font=("Constantia", 12))
        self.table_number_label.config(font=("Constantia", 12))

        self.table_number_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.table_number_entry.grid(row=1, column=1, padx=(5, 20), pady=5)
        self.table_number_entry.config(font=("Helvetica", 12))

        self.date_reservation_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.date_reservation_entry.grid(row=2, column=1, padx=(5, 20), pady=5)
        self.date_reservation_entry.config(font=("Helvetica", 12))

        self.save_font_button_border = tk.Frame(self.master,
                                                highlightbackground="#289BBB",
                                                highlightcolor="#289BBB",
                                                highlightthickness=1,
                                                bd=0)
        self.save_font_button_border.grid(row=3, column=0, padx=(0, 20), pady=(15, 15), sticky="e")

        self.cancel_button_border = tk.Frame(self.master,
                                             highlightbackground="#BB4533",
                                             highlightcolor="#BB4533",
                                             highlightthickness=1,
                                             bd=0)
        self.cancel_button_border.grid(row=3, column=1, pady=(15, 15), sticky="w")

        save_close_bt = tkFont.Font(size=10)

        self.save_font_button = tk.Button(self.save_font_button_border, text="Просмотр", command=lambda: self.create_info_table_window(InfoTable))
        self.save_font_button.grid(row=3, column=0, sticky="e")

        self.exit_button = tk.Button(self.cancel_button_border, text="Закрыть", command=self.destroy_table_window)
        self.exit_button.grid(row=3, column=1, sticky="w")

        self.save_font_button['font'] = save_close_bt
        self.exit_button['font'] = save_close_bt

    def destroy_table_window(self):
        # super_master.deiconify()
        self.master.destroy()

    def create_calendar_window(self, _class):
        calendar_window = tk.Toplevel(self.master)
        _class(calendar_window)

    def create_info_table_window(self, _class):

        if not check_valid_date_for_reservation(self.date_reservation_entry.get()):
            messagebox.showwarning(title='Error',
                                   message='Введена некоректная дата!')
            return 1

        occupied_tables_list, free_tables_list = checking_free_seats_by_time(date_res=self.date_reservation_entry.get(),
                                                                             table_number=self.table_number_entry.get())

        if not occupied_tables_list and not free_tables_list:
            messagebox.showwarning(title='Error',
                                   message='На заданный день нет никакой информации по забронированным столикам!')
            return 1

        info_table = tk.Toplevel(self.master)
        _class(info_table, self.table_number_entry.get(), self.date_reservation_entry.get())


class EmployeesListWindow:
    def __init__(self, master=None):
        self.master = master
        self.master.geometry(centering_window(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.create_widgets()

    def create_widgets(self):

        employees = get_employees_from_db()
        id_row = 0
        for employee in employees:
            if employee["permission"] == 'admin':
                emp = "Администртор"
            else:
                emp = "Метрдотель"

            l1 = tk.Label(self.master, text=f'ID: {employee["id_employee"]}; ФИО: {employee["fio"]}; Телефон: {employee["phone"]}; Паспорт: {employee["passport"]}; Токен: {employee["auth_token"]}; Полномочия: {emp}')
            l1.grid(row=id_row, column=0)
            id_row += 1

            l1.config(font=("Helvetica", 12))

        self.employee_edit_label = tk.Label(self.master, text="ID метрдотеля, которого вы хотите редактировать: ")
        self.employee_edit_label.grid(row=id_row, column=0, sticky="w", pady=(50, 20), padx=(20,0))
        self.employee_edit_label.config(font=("Helvetica", 14))

        self.employee_edit_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.employee_edit_entry.grid(row=id_row, column=0, sticky="w", padx=(550, 0), pady=(50, 20))

        edit_emp_style = ttk.Style()
        edit_emp_style.configure('myEdit.TButton', font=('Helvetica', 12))

        self.employee_edit_button = ttk.Button(self.master, style='myEdit.TButton', text="Редактировать",
                                               command=lambda: self.create_edit_employee_window(EmployeeEditWindow, self.employee_edit_entry.get()))
        self.employee_edit_button.grid(row=id_row, column=0,  sticky="e", pady=(50, 0), padx=(0, 20))

        exit_program_button_style = ttk.Style()
        exit_program_button_style.configure('myExit.TButton', font=('Helvetica', 12), background='red')
        self.exit_button = ttk.Button(self.master, style='myExit.TButton', text="Выход", command=self.destroy_table_window)
        self.exit_button.grid(row=id_row+1, column=0,  sticky="e", pady=(0, 20), padx=(0, 20))

        id_row = 0

    def create_edit_employee_window(self, _class, employee_id):
        if employee_id == '':
            messagebox.showwarning(title='Error', message='Введите ID сотрудника!')
        else:
            employee = get_employee_from_db(employee_id)
            calendar_window = tk.Toplevel(self.master)
            _class(calendar_window, id_employee=employee['id_employee'],
                   fio=employee['fio'],
                   phone=employee['phone'],
                   passport=employee['passport'],
                   auth_token=employee['auth_token'],
                   permission=employee['permission'])

    def destroy_table_window(self):
        self.master.destroy()


class EmployeeEditWindow:
    def __init__(self, master=None, id_employee=None, fio=None, phone=None, passport=None, auth_token=None, permission=None):
        self.id_employee = id_employee
        self.fio = fio
        self.phone = phone
        self.passport = passport
        self.auth_token = auth_token
        self.permission = permission

        self.master = master
        self.master.minsize(410, 270)
        self.master.maxsize(410, 270)
        self.master.geometry(centering_window(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.master.title("Редактирование работников")
        self.master.iconbitmap('media/admin.ico')
        self.create_widgets()

    def create_widgets(self):

        myLabel = tk.Label(self.master, text=f'Добавление сотрудника')
        myLabel.grid(row=0, column=0, pady=(10, 15), columnspan=2)
        myLabel.config(font=("large", 14))

        self.fio_label = tk.Label(self.master, text="ФИО сотрудника:")
        self.phone_label = tk.Label(self.master, text="Телефон:")
        self.pasport_label = tk.Label(self.master, text="Паспортные данные:")
        self.token_label = tk.Label(self.master, text="Токен авторизации:")
        self.permission_label = tk.Label(self.master, text="Полномочия:")

        self.fio_label.grid(row=1, column=0, padx=(20, 0), sticky="w")
        self.phone_label.grid(row=2, column=0, padx=(20, 0), sticky="w")
        self.pasport_label.grid(row=3, column=0, padx=(20, 0), sticky="w")
        self.token_label.grid(row=4, column=0, padx=(20, 0), sticky="w")
        self.permission_label.grid(row=5, column=0, padx=(20, 0), sticky="w")

        self.fio_label.config(font=("Constantia", 12))
        self.phone_label.config(font=("Constantia", 12))
        self.pasport_label.config(font=("Constantia", 12))
        self.token_label.config(font=("Constantia", 12))
        self.permission_label.config(font=("Constantia", 12))

        self.token_entry_text = tk.StringVar()

        self.fio_entry = tk.Entry(self.master, textvariable=self.token_entry_text)
        self.phone_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.pasport_entry = tk.Entry(self.master, textvariable=tk.StringVar())

        self.token_entry_label = tk.Label(self.master, text=self.auth_token)

        self.fio_entry.grid(row=1, column=1, padx=(5, 20), pady=5)
        self.phone_entry.grid(row=2, column=1, padx=(5, 20), pady=5)
        self.pasport_entry.grid(row=3, column=1, padx=(5, 20), pady=5)

        self.token_entry_label.grid(row=4, column=1, padx=(5, 20), pady=5, sticky="w")

        self.fio_entry.config(font=("Helvetica", 12))
        self.phone_entry.config(font=("Helvetica", 12))
        self.pasport_entry.config(font=("Helvetica", 12))

        self.fio_entry.insert(tk.END, self.fio)
        self.phone_entry.insert(tk.END, self.phone)
        self.pasport_entry.insert(tk.END, self.passport)

        self.token_entry_label.config(font=("Helvetica", 12))

        self.permission_selector = ttk.Combobox(self.master, values=PERMISSION_LIST, width=18)
        self.permission_selector.grid(row=5, column=1, padx=(5, 20))
        root.option_add('*TCombobox*Listbox.font', ("Helvetica", 12))
        self.permission_selector.config(font=("Helvetica", 12))

        if self.permission == 'worker':
            self.perm = 1
        else:
            self.perm = 0
        self.permission_selector.current(self.perm)

        self.save_font_button_border = tk.Frame(self.master,
                                                highlightbackground="#289BBB",
                                                highlightcolor="#289BBB",
                                                highlightthickness=1,
                                                bd=0)
        self.save_font_button_border.grid(row=6, column=1, padx=(30, 0), pady=(15, 15), sticky="w")

        self.cancel_button_border = tk.Frame(self.master,
                                             highlightbackground="#BB4533",
                                             highlightcolor="#BB4533",
                                             highlightthickness=1,
                                             bd=0)
        self.cancel_button_border.grid(row=6, column=1, pady=(15, 15), sticky="e")

        from tkinter import font as tkFont  # for convenience
        save_close_bt = tkFont.Font(size=10)

        self.save_font_button = tk.Button(self.save_font_button_border, text="Сохранить",
                                          command=self.edit_employee_data)
        self.save_font_button.grid(row=6, column=1, sticky="w")

        self.exit_button = tk.Button(self.cancel_button_border, text="Закрыть", command=self.destroy_table_window)
        self.exit_button.grid(row=6, column=1, sticky="e")

        self.save_font_button['font'] = save_close_bt
        self.exit_button['font'] = save_close_bt

        self.generate_token = ttk.Button(self.master, text="Сгенерировать",
                                         command=self.generate_token)

        self.generate_token.grid(row=4, column=1, sticky="e", padx=20)

    def edit_employee_data(self):
        self.get_permission = None
        if self.permission_selector.get() == 'Администратор':
            self.get_permission = 'admin'
        elif self.permission_selector.get() == 'Метрдотель':
            self.get_permission = 'worker'

        if self.get_permission is not None:
            if self.token_entry_label['text'] != '':
                if self.fio_entry.get() != '':
                    if self.phone_entry.get() != '':
                        if self.pasport_entry.get() != '':
                            edit_employee_in_db(fio=self.fio_entry.get(),
                                                  phone=self.phone_entry.get(),
                                                  passport=self.pasport_entry.get(),
                                                  auth_token=self.token_entry_label['text'],
                                                  permission=self.get_permission,
                                                  employee_id=self.id_employee)
                            self.master.destroy()
                        else:
                            messagebox.showwarning(title='Error', message='Введите паспортные данные сотрудника!')
                    else:
                        messagebox.showwarning(title='Error', message='Введите телефон сотрудника!')
                else:
                    messagebox.showwarning(title='Error', message='Введите ФИО сотрудника!')
            else:
                messagebox.showwarning(title='Error', message='Сгенерируйте токен аунтефекации!')
        else:
            messagebox.showwarning(title='Error', message='Выберете полномочия сотрудника из доступного списка!')

    def generate_token(self):
        auth_token = ''
        for _ in range(7):
            auth_token = auth_token + random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)

        self.token_entry_label['text'] = auth_token

    def destroy_table_window(self):
        self.master.destroy()


class EmployeeWindow:
    def __init__(self, master=None):
        self.master = master
        self.master.geometry(centering_window(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.master.minsize(410, 270)
        self.master.maxsize(410, 270)
        self.master.title("Добавление работников")
        self.master.iconbitmap('media/admin.ico')
        self.create_widgets()

    def create_widgets(self):

        myLabel = tk.Label(self.master, text=f'Добавление сотрудника')
        myLabel.grid(row=0, column=0, pady=(10, 15), columnspan=2)
        myLabel.config(font=("large", 14))

        self.fio_label = tk.Label(self.master, text="ФИО сотрудника:")
        self.phone_label = tk.Label(self.master, text="Телефон:")
        self.pasport_label = tk.Label(self.master, text="Паспортные данные:")
        self.token_label = tk.Label(self.master, text="Токен авторизации:")
        self.permission_label = tk.Label(self.master, text="Полномочия:")

        self.fio_label.grid(row=1, column=0, padx=(20, 0), sticky="w")
        self.phone_label.grid(row=2, column=0, padx=(20, 0), sticky="w")
        self.pasport_label.grid(row=3, column=0, padx=(20, 0), sticky="w")
        self.token_label.grid(row=4, column=0, padx=(20, 0), sticky="w")
        self.permission_label.grid(row=5, column=0, padx=(20, 0), sticky="w")

        self.fio_label.config(font=("Constantia", 12))
        self.phone_label.config(font=("Constantia", 12))
        self.pasport_label.config(font=("Constantia", 12))
        self.token_label.config(font=("Constantia", 12))
        self.permission_label.config(font=("Constantia", 12))

        self.token_entry_text = tk.StringVar()

        self.fio_entry = tk.Entry(self.master, textvariable=self.token_entry_text)
        self.phone_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.pasport_entry = tk.Entry(self.master, textvariable=tk.StringVar())

        self.token_entry_label = tk.Label(self.master, text='')

        self.fio_entry.grid(row=1, column=1, padx=(5, 20), pady=5)
        self.phone_entry.grid(row=2, column=1, padx=(5, 20), pady=5)
        self.pasport_entry.grid(row=3, column=1, padx=(5, 20), pady=5)

        self.token_entry_label.grid(row=4, column=1, padx=(5, 20), pady=5, sticky="w")

        self.fio_entry.config(font=("Helvetica", 12))
        self.phone_entry.config(font=("Helvetica", 12))
        self.pasport_entry.config(font=("Helvetica", 12))

        self.token_entry_label.config(font=("Helvetica", 12))

        self.permission_selector = ttk.Combobox(self.master, values=PERMISSION_LIST, width=18)
        self.permission_selector.grid(row=5, column=1, padx=(5, 20))
        root.option_add('*TCombobox*Listbox.font', ("Helvetica", 12))
        self.permission_selector.config(font=("Helvetica", 12))

        self.save_font_button_border = tk.Frame(self.master,
                                                highlightbackground="#289BBB",
                                                highlightcolor="#289BBB",
                                                highlightthickness=1,
                                                bd=0)
        self.save_font_button_border.grid(row=6, column=1, padx=(30, 0), pady=(15, 15), sticky="w")

        self.cancel_button_border = tk.Frame(self.master,
                                             highlightbackground="#BB4533",
                                             highlightcolor="#BB4533",
                                             highlightthickness=1,
                                             bd=0)
        self.cancel_button_border.grid(row=6, column=1, pady=(15, 15), sticky="e")

        from tkinter import font as tkFont  # for convenience
        save_close_bt = tkFont.Font(size=10)

        self.save_font_button = tk.Button(self.save_font_button_border, text="Сохранить",
                                          command=self.save_employee_data)
        self.save_font_button.grid(row=6, column=1, sticky="w")

        self.exit_button = tk.Button(self.cancel_button_border, text="Закрыть", command=self.destroy_table_window)
        self.exit_button.grid(row=6, column=1, sticky="e")

        self.save_font_button['font'] = save_close_bt
        self.exit_button['font'] = save_close_bt

        self.generate_token = ttk.Button(self.master, text="Сгенерировать",
                                         command=self.generate_token)

        self.generate_token.grid(row=4, column=1, sticky="e", padx=20)

    def save_employee_data(self):
        self.get_permission = None
        if self.permission_selector.get() == 'Администратор':
            self.get_permission = 'admin'
        elif self.permission_selector.get() == 'Метрдотель':
            self.get_permission = 'worker'

        if self.get_permission is not None:
            if self.token_entry_label['text'] != '':
                if self.fio_entry.get() != '':
                    if self.phone_entry.get() != '':
                        if self.pasport_entry.get() != '':
                            create_employee_in_db(fio=self.fio_entry.get(),
                                                  phone=self.phone_entry.get(),
                                                  passport=self.pasport_entry.get(),
                                                  auth_token=self.token_entry_label['text'],
                                                  permission=self.get_permission)
                            self.master.destroy()
                        else:
                            messagebox.showwarning(title='Error', message='Введите паспортные данные сотрудника!')
                    else:
                        messagebox.showwarning(title='Error', message='Введите телефон сотрудника!')
                else:
                    messagebox.showwarning(title='Error', message='Введите ФИО сотрудника!')
            else:
                messagebox.showwarning(title='Error', message='Сгенерируйте токен аунтефекации!')
        else:
            messagebox.showwarning(title='Error', message='Выберете полномочия сотрудника из доступного списка!')

    def generate_token(self):
        auth_token = ''
        for _ in range(7):
            auth_token = auth_token + random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)

        self.token_entry_label['text'] = auth_token

    def destroy_table_window(self):
        self.master.destroy()


class MainWindow:
    def __init__(self, master=None, employee_id=None):
        self.master = master
        self.master.attributes('-fullscreen', True)
        self.fullScreenState = False
        self.employee_id = employee_id

        self.master.title("Бронирование столиков")

        self.create_widgets()

    def create_widgets(self):
        self.table_photo_1 = tk.PhotoImage(file="images/img_1.png")
        self.table_photo_2 = tk.PhotoImage(file="images/img_2.png")
        self.table_photo_3 = tk.PhotoImage(file="images/img_3.png")
        self.table_photo_4 = tk.PhotoImage(file="images/img_4.png")
        self.table_photo_5 = tk.PhotoImage(file="images/img_5.png")
        self.table_photo_6 = tk.PhotoImage(file="images/img_6.png")
        self.table_photo_7 = tk.PhotoImage(file="images/img_7.png")
        self.table_photo_8 = tk.PhotoImage(file="images/img_8.png")
        self.table_photo_9 = tk.PhotoImage(file="images/img_9.png")
        self.table_photo_10 = tk.PhotoImage(file="images/img_10.png")
        self.table_photo_11 = tk.PhotoImage(file="images/img_11.png")
        self.table_photo_12 = tk.PhotoImage(file="images/img_12.png")
        self.table_photo_13 = tk.PhotoImage(file="images/img_13.png")
        self.table_photo_14 = tk.PhotoImage(file="images/img_14.png")

        self.fio_employee = tk.Label(self.master, text=f"Сотрудник - {get_fio_employee(employee_id=self.employee_id)}")
        self.fio_employee.grid(row=0, column=0, pady=(80, 0), columnspan=2)
        self.fio_employee.config(font=("Constantia", 18))

        exit_program_button_style = ttk.Style()
        exit_program_button_style.configure('myS.TButton', font=('Helvetica', 12), background='red')
        self.exit_program_button = ttk.Button(self.master, text="Выход", style='myS.TButton', command=self.exit_program)
        self.exit_program_button.grid(row=0, column=4, pady=(80, 0), columnspan=2)

        self.b1 = tk.Button(self.master, text="Столик 1", image=self.table_photo_1,
                            command=lambda: self.create_table_window(TableWindow, 1))
        self.b1.grid(row=1, column=0, padx=(200, 20), pady=(100, 20))

        self.b2 = tk.Button(self.master, text="Столик 2", image=self.table_photo_2,
                            command=lambda: self.create_table_window(TableWindow, 2))
        self.b2.grid(row=1, column=1, padx=(20, 75), pady=(100, 20))

        self.b3 = tk.Button(self.master, text="Столик 3", image=self.table_photo_3,
                            command=lambda: self.create_table_window(TableWindow, 3))
        self.b3.grid(row=2, column=0, padx=(200, 20), pady=20)

        self.b4 = tk.Button(self.master, text="Столик 4", image=self.table_photo_4,
                            command=lambda: self.create_table_window(TableWindow, 4))
        self.b4.grid(row=2, column=1, padx=(20, 75), pady=20)

        self.b5 = tk.Button(self.master, text="Столик 5", image=self.table_photo_5,
                            command=lambda: self.create_table_window(TableWindow, 5))
        self.b5.grid(row=3, column=0, padx=(200, 20), pady=20)

        self.b6 = tk.Button(self.master, text="Столик 6", image=self.table_photo_6,
                            command=lambda: self.create_table_window(TableWindow, 6))
        self.b6.grid(row=3, column=1, padx=(20, 75), pady=20)
        #
        #
        #
        self.b7 = tk.Button(self.master, text="Столик 7", image=self.table_photo_7,
                            command=lambda: self.create_table_window(TableWindow, 7))
        self.b7.grid(row=1, column=2, padx=20, pady=(100, 20), columnspan=2)

        self.b8 = tk.Button(self.master, text="Столик 8", image=self.table_photo_8,
                            command=lambda: self.create_table_window(TableWindow, 8))
        self.b8.grid(row=3, column=2, padx=20, pady=20)

        self.b9 = tk.Button(self.master, text="Столик 9", image=self.table_photo_9,
                            command=lambda: self.create_table_window(TableWindow, 9))
        self.b9.grid(row=3, column=3, padx=20, pady=20)
        #
        #
        #
        self.b10 = tk.Button(self.master, text="Столик 10", image=self.table_photo_10,
                             command=lambda: self.create_table_window(TableWindow, 10))
        self.b10.grid(row=1, column=4, padx=(75, 20), pady=(100, 20))

        self.b11 = tk.Button(self.master, text="Столик 11", image=self.table_photo_11,
                             command=lambda: self.create_table_window(TableWindow, 11))
        self.b11.grid(row=1, column=5, padx=20, pady=(100, 20))

        self.b12 = tk.Button(self.master, text="Столик 12", image=self.table_photo_12,
                             command=lambda: self.create_table_window(TableWindow, 12))
        self.b12.grid(row=2, column=5, padx=20, pady=20)

        self.b13 = tk.Button(self.master, text="Столик 13", image=self.table_photo_13,
                             command=lambda: self.create_table_window(TableWindow, 13))
        self.b13.grid(row=3, column=4, padx=(75, 20), pady=20)

        self.b14 = tk.Button(self.master, text="Столик 14", image=self.table_photo_14,
                             command=lambda: self.create_table_window(TableWindow, 14))
        self.b14.grid(row=3, column=5, padx=20, pady=20)

    def create_table_window(self, _class, table_number):
        # костыль на инвиз main окна
        global super_master
        super_master = self.master

        # self.master.withdraw()

        table_window = tk.Toplevel(self.master)

        # ???????????молчу
        global table_window_instance
        table_window_instance = _class(table_window, table_number)

    def exit_program(self):
        sys.exit()


class TableWindow:
    def __init__(self, master=None, table_number=None):
        self.master = master
        self.table_number = table_number

        self.master.geometry(centering_window(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.master.minsize(527, 430)
        self.master.maxsize(527, 430)

        # self.master.geometry('600x400+200+100')
        # self.master.maxsize(width=420, height=300)  # fixed window size
        # self.master.minsize(width=420, height=300)

        self.date_reservation_entry = None

        self.master.title(f"Бронирование столика № {self.table_number}")
        self.master.iconbitmap('media/res_table.ico')

        self.create_widgets()

    def create_widgets(self):
        table = tk.Label(self.master, text=f'Столик под номером {self.table_number}')
        table.grid(row=0, column=0, pady=(15, 20), columnspan=2)
        table.config(font=("large", 20))

        self.date_reservation_label = tk.Label(self.master, text="Дата:")
        self.time_reservation_label = tk.Label(self.master, text="Время:")
        self.clients_number_label = tk.Label(self.master, text="Количество человек:")
        self.name_label = tk.Label(self.master, text="Имя клиента:")
        self.surname_label = tk.Label(self.master, text="Фамилия клиента:")
        self.phone_number_label = tk.Label(self.master, text="Мобильный телефон:")
        self.email_label = tk.Label(self.master, text="Email:")

        self.date_reservation_label.grid(row=1, column=0, padx=(20, 0), sticky="w")
        self.time_reservation_label.grid(row=2, column=0, padx=(20, 0), sticky="w")
        self.clients_number_label.grid(row=3, column=0, padx=(20, 0), sticky="w")
        self.name_label.grid(row=4, column=0, padx=(20, 0), sticky="w")
        self.surname_label.grid(row=5, column=0, padx=(20, 0), sticky="w")
        self.phone_number_label.grid(row=6, column=0, padx=(20, 0), sticky="w")
        self.email_label.grid(row=7, column=0, padx=(20, 0), sticky="w")

        self.date_reservation_label.config(font=("Constantia", 12))
        self.time_reservation_label.config(font=("Constantia", 12))
        self.clients_number_label.config(font=("Constantia", 12))
        self.name_label.config(font=("Constantia", 12))
        self.surname_label.config(font=("Constantia", 12))
        self.phone_number_label.config(font=("Constantia", 12))
        self.email_label.config(font=("Constantia", 12))

        # variable = tk.StringVar(self.master)
        # variable.set(get_current_time_in_database_format())
        # a = ["one", "two", "three"]
        # self.w = tk.OptionMenu(self.master, variable, *a)

        self.date_reservation_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.clients_number_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.name_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.surname_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.phone_number_entry = tk.Entry(self.master, textvariable=tk.StringVar())
        self.email_entry = tk.Entry(self.master, textvariable=tk.StringVar())


        self.comment_label = tk.Label(self.master, text="Комментарий к заказу:")
        self.comment_label.grid(row=8, column=0)
        self.comment_label.config(font=("Constantia", 12))

        self.comment_text = tk.Text(self.master, height=5, width=25)
        self.comment_text.grid(row=8, column=1)

        self.date_reservation_entry.grid(row=1, column=1, padx=(5, 20), pady=5)
        self.clients_number_entry.grid(row=3, column=1, padx=(5, 20), pady=5)
        self.name_entry.grid(row=4, column=1, padx=(5, 20), pady=5)
        self.surname_entry.grid(row=5, column=1, padx=(5, 20), pady=5)
        self.phone_number_entry.grid(row=6, column=1, padx=(5, 20), pady=5)
        self.email_entry.grid(row=7, column=1, padx=(5, 20), pady=5)


        self.date_reservation_entry.config(font=("Helvetica", 12))
        self.clients_number_entry.config(font=("Helvetica", 12))
        self.name_entry.config(font=("Helvetica", 12))
        self.surname_entry.config(font=("Helvetica", 12))
        self.phone_number_entry.config(font=("Helvetica", 12))
        self.email_entry.config(font=("Helvetica", 12))

        self.save_font_button_border = tk.Frame(self.master,
                                                highlightbackground="#289BBB",
                                                highlightcolor="#289BBB",
                                                highlightthickness=1,
                                                bd=0)
        self.save_font_button_border.grid(row=9, column=1, padx=(0, 20), pady=(15, 15), sticky="e")

        self.cancel_button_border = tk.Frame(self.master,
                                             highlightbackground="#BB4533",
                                             highlightcolor="#BB4533",
                                             highlightthickness=1,
                                             bd=0)
        self.cancel_button_border.grid(row=9, column=2, pady=(15, 15), sticky="w")

        save_close_bt = tkFont.Font(size=10)

        self.save_font_button = tk.Button(self.save_font_button_border, text="Сохранить", command=self.save_data)
        self.save_font_button.grid(row=9, column=1, sticky="e")

        self.exit_button = tk.Button(self.cancel_button_border, text="Закрыть", command=self.destroy_table_window)
        self.exit_button.grid(row=9, column=2, sticky="w")

        self.save_font_button['font'] = save_close_bt
        self.exit_button['font'] = save_close_bt

        calendar_button_style = ttk.Style()
        calendar_button_style.configure('my.TButton', font=('Helvetica', 12))
        self.calendar_button = ttk.Button(self.master, text="Календарь", style='my.TButton',
                                          command=lambda: self.create_calendar_window(CalendarWindow))
        self.calendar_button.grid(row=1, column=2, padx=(0, 20))

        self.time_selector = ttk.Combobox(self.master, values=TIME_RESERVATION, width=18)
        self.time_selector.grid(row=2, column=1, padx=(5, 20))
        root.option_add('*TCombobox*Listbox.font', ("Helvetica", 12))
        self.time_selector.config(font=("Helvetica", 12))

        self.info_table = ttk.Button(self.master, text="Информация", style='my.TButton',
                                     command=lambda: self.create_info_table_window(InfoTable))
        self.info_table.grid(row=0, column=2, sticky='w')


    def save_data(self):
        if check_valid_email_address(email=self.email_entry.get()):
            if check_valid_phone_number(phone_number=self.phone_number_entry.get()):
                if self.clients_number_entry.get() != '':
                    if check_table_places_in_db(int(self.table_number), int(self.clients_number_entry.get())):
                        if check_valid_date(self.date_reservation_entry.get()):
                            check, date_start, date_end = check_for_a_week(self.date_reservation_entry.get())
                            if check:
                                if self.time_selector.get() in TIME_RESERVATION:
                                    occupied_tables_list, _ = checking_free_seats_by_time(date_res=self.date_reservation_entry.get(),
                                                                                          table_number=self.table_number)
                                    if f'{self.time_selector.get()}:00' not in occupied_tables_list:
                                        if self.name_entry.get() != '':
                                            # сохранение данных о клиенте в базу данных
                                            insert_data_into_client_db(name=self.name_entry.get(),
                                                                       surname=self.surname_entry.get(),
                                                                       phone=self.phone_number_entry.get(),
                                                                       email=self.email_entry.get(),)

                                            insert_data_into_reservation_db(date_res=self.date_reservation_entry.get(),
                                                                            table_number=int(self.table_number),
                                                                            client_number=self.clients_number_entry.get(),
                                                                            time_res=self.time_selector.get(),
                                                                            comment=self.comment_text.get("1.0",'end-1c'))
                                            self.destroy_table_window()
                                        else:
                                            messagebox.showwarning(title='Error',
                                                                   message=f'Введите имя клиента!')
                                    else:
                                        messagebox.showwarning(title='Error',
                                                           message=f'Столик под номером {self.table_number} уже забронирован на {self.time_selector.get()}!')
                                else:
                                    messagebox.showwarning(title='Error',
                                                          message=f'Введите время бронирования из доступного списка времени!')
                            else:
                                messagebox.showwarning(title='Error',
                                                       message=f'Вы можете бронировать столики с {date_start} - {date_end}!')
                        else:
                            messagebox.showwarning(title='Error',
                                                   message='Введите корректную дату бронирования!')
                    else:
                        messagebox.showwarning(title='Error',
                                               message='Количество человек больше, чем мест за столиком!')
                else:
                    messagebox.showwarning(title='Error',
                                           message='Введите кол-во человек за столиком!')


            else:
                messagebox.showwarning(title='Error', message='Неправильно введен номер телефона!')

        else:
            messagebox.showwarning(title='Error', message='Неправильно введен E-mail адрес!')

    def destroy_table_window(self):
        # super_master.deiconify()
        self.master.destroy()

    def create_calendar_window(self, _class):
        calendar_window = tk.Toplevel(self.master)
        _class(calendar_window)

    def create_info_table_window(self, _class):

        if not check_valid_date_for_reservation(self.date_reservation_entry.get()):
            messagebox.showwarning(title='Error',
                                   message='Введена некоректная дата!')
            return 1

        occupied_tables_list, free_tables_list = checking_free_seats_by_time(date_res=self.date_reservation_entry.get(),
                                                                             table_number=self.table_number)

        if not occupied_tables_list and not free_tables_list:
            messagebox.showwarning(title='Error',
                                   message='На заданный день нет никакой информации по забронированным столикам!')
            return 1


        calendar_window = tk.Toplevel(self.master)
        _class(calendar_window, self.table_number, self.date_reservation_entry.get())


class CalendarWindow:
    def __init__(self, master=None):
        self.master = master
        self.master.geometry(centering_window(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.create_widgets()

    def create_widgets(self):
        current_data = get_current_time_in_database_format().split(" ")[0].split("-")
        self.cal = Calendar(self.master,
                            font="Arial 14", selectmode='day', year=int(current_data[0]), month=int(current_data[1]),
                            day=int(current_data[2]))
        self.cal.pack(fill="both", expand=True)
        ttk.Button(self.master, text="ok", command=self.save_date_and_destroy_calendar_window).pack()

    def save_date_and_destroy_calendar_window(self):
        table_window_instance.date_reservation_entry.delete(0, tk.END)
        table_window_instance.date_reservation_entry.insert(0, self.cal.selection_get())
        self.master.destroy()


class InfoTable:
    def __init__(self, master=None, table_number=None, date_res=None):
        self.table_number = table_number
        self.date_res = date_res
        self.master = master
        self.master.geometry(centering_window(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.master.minsize(480, 230)
        self.master.maxsize(480, 230)
        self.master.title(f"Информация по столику № {self.table_number}")
        self.master.iconbitmap('media/res_table.ico')
        self.create_widgets()

    def create_widgets(self):

        occupied_tables_list, free_tables_list = checking_free_seats_by_time(date_res=self.date_res,
                                                                             table_number=self.table_number)

        self.time_1 = tk.Label(self.master, text="9:00")
        self.time_2 = tk.Label(self.master, text="9:30")
        self.time_3 = tk.Label(self.master, text="10:00")
        self.time_4 = tk.Label(self.master, text="10:30")
        self.time_5 = tk.Label(self.master, text="11:00")
        self.time_6 = tk.Label(self.master, text="11:30")
        self.time_7 = tk.Label(self.master, text="12:00")
        self.time_8 = tk.Label(self.master, text="12:30")
        self.time_9 = tk.Label(self.master, text="13:00")
        self.time_10 = tk.Label(self.master, text="13:30")
        self.time_11 = tk.Label(self.master, text="14:00")
        self.time_12 = tk.Label(self.master, text="14:30")
        self.time_13 = tk.Label(self.master, text="15:00")
        self.time_14 = tk.Label(self.master, text="15:30")
        self.time_15 = tk.Label(self.master, text="16:00")
        self.time_16 = tk.Label(self.master, text="16:30")
        self.time_17 = tk.Label(self.master, text="17:00")
        self.time_18 = tk.Label(self.master, text="17:30")
        self.time_19 = tk.Label(self.master, text="18:00")
        self.time_20 = tk.Label(self.master, text="18:30")
        self.time_21 = tk.Label(self.master, text="19:00")
        self.time_22 = tk.Label(self.master, text="19:30")
        self.time_23 = tk.Label(self.master, text="20:00")
        self.time_24 = tk.Label(self.master, text="20:30")
        self.time_25 = tk.Label(self.master, text="21:00")

        self.time_1.grid(row=1, column=0, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_2.grid(row=1, column=1, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_3.grid(row=1, column=2, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_4.grid(row=1, column=3, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_5.grid(row=1, column=4, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_6.grid(row=2, column=0, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_7.grid(row=2, column=1, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_8.grid(row=2, column=2, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_9.grid(row=2, column=3, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_10.grid(row=2, column=4, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_11.grid(row=3, column=0, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_12.grid(row=3, column=1, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_13.grid(row=3, column=2, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_14.grid(row=3, column=3, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_15.grid(row=3, column=4, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_16.grid(row=4, column=0, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_17.grid(row=4, column=1, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_18.grid(row=4, column=2, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_19.grid(row=4, column=3, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_20.grid(row=4, column=4, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_21.grid(row=5, column=0, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_22.grid(row=5, column=1, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_23.grid(row=5, column=2, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_24.grid(row=5, column=3, sticky="we", padx=(5, 5), pady=(5, 5))
        self.time_25.grid(row=5, column=4, sticky="we", padx=(5, 5), pady=(5, 5))

        self.time_list = []
        self.time_list.append(self.time_1)
        self.time_list.append(self.time_2)
        self.time_list.append(self.time_3)
        self.time_list.append(self.time_4)
        self.time_list.append(self.time_5)
        self.time_list.append(self.time_6)
        self.time_list.append(self.time_7)
        self.time_list.append(self.time_8)
        self.time_list.append(self.time_9)
        self.time_list.append(self.time_10)
        self.time_list.append(self.time_11)
        self.time_list.append(self.time_12)
        self.time_list.append(self.time_13)
        self.time_list.append(self.time_14)
        self.time_list.append(self.time_15)
        self.time_list.append(self.time_16)
        self.time_list.append(self.time_17)
        self.time_list.append(self.time_18)
        self.time_list.append(self.time_19)
        self.time_list.append(self.time_20)
        self.time_list.append(self.time_21)
        self.time_list.append(self.time_22)
        self.time_list.append(self.time_23)
        self.time_list.append(self.time_24)
        self.time_list.append(self.time_25)


        for cur_time in self.time_list:
            if f'{cur_time.cget("text")}:00' in occupied_tables_list:
                cur_time.config({"background": "Red"}, font=("Courier", 20))

            elif f'{cur_time.cget("text")}:00' in free_tables_list:
                cur_time.config({"background": "Green"}, font=("Courier", 20))




if __name__ == "__main__":
    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    root = tk.Tk()

    root.eval('tk::PlaceWindow . center')

    root.title("Авторизация")
    root.iconbitmap('media/auth.ico')

    app = LoginWindow(master=root)

    root.mainloop()
