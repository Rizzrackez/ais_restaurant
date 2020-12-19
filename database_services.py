import pymysql.cursors
import main_services

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='maksim2212',
                             db='db_reservation',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_fio_employee(employee_id):
    try:
        with connection.cursor() as cursor:
            get_client_sql = 'SELECT fio FROM db_reservation.employee WHERE id_employee = %s;'
            cursor.execute(get_client_sql, int(employee_id))
            fio_employee = cursor.fetchone()

            return fio_employee['fio']

    finally:
        pass


def check_table_places_in_db(table_number, clients_number):
    """SELECT places FROM db_reservation.table WHERE table_number = 1;"""
    try:
        with connection.cursor() as cursor:
            get_client_sql = 'SELECT places FROM db_reservation.table WHERE table_number = %s;'
            cursor.execute(get_client_sql, table_number)
            last_client_in_db = cursor.fetchone()

            places = int(last_client_in_db['places'])
            if clients_number < 0:
                return False
            return places >= clients_number

    finally:
        pass


def insert_data_into_client_db(name, surname, phone, email):
    try:
        with connection.cursor() as cursor:
            sql = "insert into client (`name`, `surname`, `phone`, `email`) values (%s, %s, %s, %s);"
            cursor.execute(sql, (name, surname, phone, email))
            connection.commit()
    finally:
        pass


def insert_data_into_reservation_db(date_res, time_res, table_number, client_number, comment=''):

    try:
        with connection.cursor() as cursor:
            get_client_sql = 'select id_client from client ORDER BY id_client desc limit 1;'
            cursor.execute(get_client_sql)
            last_client_in_db = cursor.fetchone()
            id_client = last_client_in_db['id_client']

            insert_reservation_sql = "update db_reservation.reservation " \
                                     "set comment=%s, clients_number=%s, id_client=%s, employee=1 " \
                                     "where table_number = %s and date_res = %s and time_res = %s;"
            cursor.execute(insert_reservation_sql, (comment, client_number, id_client, table_number, date_res, time_res))
            connection.commit()
    finally:
        pass


def checking_free_seats_by_time(date_res, table_number) -> (list, list):
    try:
        with connection.cursor() as cursor:
            occupied_tables_list = []
            if date_res == '':
                date_res = main_services.get_current_time_in_database_format().split(" ")[0]

            get_client_sql = "select time_res FROM reservation where date_res = %s and table_number = %s and employee is not NULL;"
            cursor.execute(get_client_sql, (date_res, table_number))

            time_res = cursor.fetchone()

            while time_res is not None:
                occupied_tables_list.append(time_res)
                time_res = cursor.fetchone()

            occupied_tables_list = [str(elem['time_res']) for elem in occupied_tables_list]

            free_tables_list = []

            get_client_sql = "select time_res FROM reservation where date_res = %s and table_number = %s and employee is NULL;"
            cursor.execute(get_client_sql, (date_res, table_number))

            time_res = cursor.fetchone()

            while time_res is not None:
                free_tables_list.append(time_res)
                time_res = cursor.fetchone()

            free_tables_list = [str(elem['time_res']) for elem in free_tables_list]

            return occupied_tables_list, free_tables_list

    finally:
        pass
    # select time_res FROM reservation where date_res = '2020-12-06' and table_number = 1 and employee is not NULL;
    # select time_res FROM reservation where date_res = '2020-12-06' and employee is NULL;


def login_verification_in_db(phone, auth_token):
    try:
        with connection.cursor() as cursor:
            get_client_sql = 'select id_employee, permission from employee where phone = %s and auth_token = %s;'
            cursor.execute(get_client_sql, (phone, auth_token))
            employee_id = cursor.fetchone()
            if employee_id != None:
                return [employee_id['id_employee'], employee_id['permission']]
            else:
                return None

    finally:
        pass


def create_employee_in_db(fio, phone, passport, auth_token, permission):
    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO db_reservation.employee (fio, phone, passport, auth_token, permission) VALUES (%s, %s, %s, %s, %s);'
            cursor.execute(sql, (fio, phone, passport, auth_token, permission))
            connection.commit()
    finally:
        pass


def edit_employee_in_db(employee_id, fio, phone, passport, auth_token, permission):
    try:
        with connection.cursor() as cursor:
            sql = 'UPDATE `db_reservation`.`employee` SET `fio` = %s, `phone` = %s, `passport` = %s, `auth_token` = %s, `permission` = %s WHERE `id_employee` = %s;'
            cursor.execute(sql, (fio, phone, passport, auth_token, permission, employee_id))
            connection.commit()
    finally:
        pass


def get_employees_from_db():
    try:
        with connection.cursor() as cursor:
            employees_list = []

            get_client_sql = "select * FROM `employee`;"
            cursor.execute(get_client_sql)

            emp = cursor.fetchone()

            while emp is not None:
                employees_list.append(emp)
                emp = cursor.fetchone()

            return employees_list

    finally:
        pass


def get_reservations_from_db(table_number=None, date_res=None, employee=None):
    if table_number == None or table_number == '':
        table_number = 'ANY(select table_number from `reservation`)'
    if employee == None or employee == '':
        employee = 'ANY(select employee from `reservation`)'
    if date_res == None or date_res == '':
        date_res = 'ANY(select date_res from `reservation`)'
    else:
        date_res = f"'{date_res}'"

    try:
        with connection.cursor() as cursor:
            reservations_list = []

            sql = f"SELECT date_res, time_res, table_number," \
                  f" (select name from `client` where `client`.id_client=`reservation`.id_client) as 'client_name'," \
                  f" (select surname from `client` where `client`.id_client=`reservation`.id_client) as 'client_surname'," \
                  f" (select phone from `client` where `client`.id_client=`reservation`.id_client) as 'client_phone', " \
                  f" clients_number, employee, comment FROM db_reservation.reservation where `reservation`.table_number = {table_number}" \
                  f" and `reservation`.date_res = {date_res} and `reservation`.employee = {employee} and employee is not null;"
            cursor.execute(sql)

            res = cursor.fetchone()

            while res is not None:
                reservations_list.append(res)
                res = cursor.fetchone()

            return reservations_list

    finally:
        pass


def get_employee_from_db(employee_id):
    try:
        with connection.cursor() as cursor:
            get_client_sql = 'select * from employee where id_employee=%s;'
            cursor.execute(get_client_sql, employee_id)
            employee = cursor.fetchone()
            return employee


    finally:
        pass


if __name__ == '__main__':
    print(get_reservations_from_db())
