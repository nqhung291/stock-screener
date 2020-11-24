from analysis import ta
from crawler import DataCrawler
from db import db


def run_daily_crawl(screen_date):
    bounce_watch_list, bounce_enter_list, ip_watch_list, ip_enter_list = ta.screener(screen_date)
    print('Bounce WATCHING list |', screen_date, bounce_watch_list)
    print('Impulse pullback WATCHING list |', screen_date, ip_watch_list)
    print('Bounce ENTER list |', screen_date, bounce_enter_list)
    print('Impulse pullback ENTER list |', screen_date, ip_enter_list)
    print('=====================================')


def get_latest_day():
    print(db.get_max_date())


if __name__ == '__main__':
    crawler = DataCrawler.DataCrawler('VCB', start_date='2020-11-18', end_date='2020-11-20')
    crawler.crawl()
