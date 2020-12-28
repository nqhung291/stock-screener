from datetime import timedelta, date
from analysis import ta


def daterange(start_date, end_date):
    date_range = []
    for n in range(int((end_date - start_date).days) + 1):
        if (start_date + timedelta(n)).weekday() < 5:
            date_range.append(start_date + timedelta(n))
    return date_range


def get_screen_result(start_date=date.today(), end_date=date.today()):
    for screen_date in daterange(start_date, end_date):
        bounce_watch_list, bounce_enter_list, ip_watch_list, ip_enter_list = ta.screener(screen_date)
        result = f'Screener result on {screen_date}:\nBounce WATCHING list {bounce_watch_list}' \
                 f'\nImpulse pullback WATCHING list {ip_watch_list} \n' \
                 f'Bounce ENTER list {bounce_enter_list} \nImpulse pullback ENTER list {ip_enter_list}'
        print('====================')
        print(result)
