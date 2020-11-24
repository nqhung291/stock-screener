from crawler import DataCrawler
from db import db
import json
from analysis import ta
from datetime import date
import datetime
from crawler import utils


def load_stock_list(exchange):
    with open('./crawler/stock_list.json') as json_file:
        data = json.load(json_file)
        return data[str.lower(exchange)]


def save_stock_list():
    exchange = 'HNX'
    stock_list = load_stock_list(exchange)
    stock_list_tuple = [(stock, exchange) for stock in sorted(stock_list)]
    db.save_stock_list(stock_list_tuple)


def crawl(exchange=None, start_date=date.today().strftime(utils.DATE_FORMAT), end_date=date.today().strftime(utils.DATE_FORMAT)):
    for (stock, exchange) in db.get_stock_symbol(exchange):
        crawler = DataCrawler.DataCrawler(stock, start_date=start_date, end_date=end_date)
        data = crawler.crawl()
        if data is not None:
            db.insert_stock_price(data)
            print('done crawl', exchange, ':', stock, 'from:', start_date, 'to:', end_date)
        else:
            print('ERROR crawl', exchange, ':', stock, 'from:', start_date, 'to:', end_date)


def run_daily_crawl():
    latest_date = db.get_max_date()
    end_date = date.today()
    if datetime.datetime.now().hour < 16:
        end_date = date.today() - datetime.timedelta(days=1)
    if date.today().weekday() > 4:
        delta = datetime.timedelta(date.today().weekday() - 4)
        end_date = date.today() - delta
        if latest_date < end_date:
            start_date = (latest_date + datetime.timedelta(days=1)).strftime(utils.DATE_FORMAT)
            crawl(start_date=start_date, end_date=end_date.strftime(utils.DATE_FORMAT))
    elif latest_date < date.today() - datetime.timedelta(days=1) or \
            (latest_date == date.today() - datetime.timedelta(days=1) and datetime.datetime.today().hour > 16):
        start_date = (latest_date + datetime.timedelta(days=1)).strftime(utils.DATE_FORMAT)
        crawl(start_date=start_date, end_date=end_date.strftime(utils.DATE_FORMAT))
    screen_date = latest_date
    bounce_watch_list, bounce_enter_list, ip_watch_list, ip_enter_list = ta.screener(screen_date)
    result = f'Screener result on {screen_date}:\nBounce WATCHING list {bounce_watch_list}' \
             f'\nImpulse pullback WATCHING list {ip_watch_list} \n' \
             f'Bounce ENTER list {bounce_enter_list} \nImpulse pullback ENTER list {ip_enter_list}'
    print(result)


if __name__ == '__main__':
    run_daily_crawl()
