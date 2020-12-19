from datetime import datetime, date, timedelta
import re
import time
import calendar


def check_for_a_week(date_res):
    date_res = date_res.split('-')
    date_res = date(int(date_res[0]), int(date_res[1]), int(date_res[2]))
    today = date.today()
    next_week_date = today + timedelta(days=7)

    if today <= next_week_date:
        return today <= date_res <= next_week_date, today, next_week_date
    else:
        return today <= date_res or date_res <= next_week_date, today, next_week_date



def check_valid_date(date):
    try:
        valid_date = time.strptime(date, '%Y-%m-%d')
        current_date = time.strptime(get_current_time_in_database_format()[0:10], '%Y-%m-%d')
        if current_date > valid_date:
            return False
        return True
    except ValueError:
        return False


def check_valid_date_for_reservation(date):
    try:
        valid_date = time.strptime(date, '%Y-%m-%d')
        current_date = time.strptime(get_current_time_in_database_format()[0:10], '%Y-%m-%d')
        return True
    except:
        return False


def get_current_time_in_database_format():
    """формат YYYY-MM-DD HH:MM:SS"""

    current_time = datetime.now()
    return f'{current_time.year}-{current_time.month}-{(lambda: current_time.day if len(str(current_time.day)) == 2 else f"0{current_time.day}")()} ' \
           f'{current_time.hour}:{current_time.minute}:{(lambda: current_time.second if len(str(current_time.second)) == 2 else f"0{current_time.second}")()}'


def check_valid_email_address(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


def check_valid_phone_number(phone_number):
    if phone_number == '':
        return False
    return all([c.isdigit() or c == '/' for c in phone_number])


def centering_window(width, height):
    w = width
    h = height
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 200  # смещение от середины
    h = h - 200

    return '+{}+{}'.format(w, h)

if __name__ == '__main__':
   a, b, c = check_for_a_week('2020-12-27')
   print(a, b, c)