from analysis import ta
from datetime import date, timedelta


def run_daily_crawl(screen_date):
    bounce_watch_list, bounce_enter_list, ip_watch_list, ip_enter_list = ta.screener(screen_date)
    print('Bounce WATCHING list |', screen_date, bounce_watch_list)
    print('Impulse pullback WATCHING list |', screen_date, ip_watch_list)
    print('Bounce ENTER list |', screen_date, bounce_enter_list)
    print('Impulse pullback ENTER list |', screen_date, ip_enter_list)
    print('=====================================')


if __name__ == '__main__':
    start_date = date(2020, 7, 20)
    end_date = date(2020, 7, 24)
    delta = timedelta(days=1)
    while start_date <= end_date:
        if start_date.weekday() not in [5, 6]:
            run_daily_crawl(start_date)
        start_date += delta
