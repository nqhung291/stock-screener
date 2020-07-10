from crawler import DataCrawler
from db import db
import json
from analysis import ta
from datetime import datetime, date, timedelta


def load_stock_list(exchange):
    with open('./crawler/stock_list.json') as json_file:
        data = json.load(json_file)
        return data[str.lower(exchange)]


def save_stock_list():
    stock_list = load_stock_list('hose')
    stock_list_tuple = [tuple(stock.split()) for stock in sorted(stock_list)]
    print(stock_list_tuple)
    db.save_stock_list(stock_list_tuple)


def crawl(crawl_date=date.today().strftime("%d/%m/%Y")):
    for stock in db.get_stock_symbol():
        crawler = DataCrawler.DataCrawler(stock, start_date=crawl_date, end_date=crawl_date)
        data = crawler.crawl()
        if data is not None:
            db.insert_stock_price(data)
            print('done crawl', stock)
        else:
            print('crawl error', stock)


def crawl_one_stock():
    crawler = DataCrawler.DataCrawler('VCB', start_date='11/06/2020', end_date='12/06/2020')
    data = crawler.crawl()
    if data is not None:
        db.insert_stock_price(data)
    print(data)


if __name__ == '__main__':
    crawl()
    bounce_watch_list, bounce_enter_list, ip_watch_list = ta.screener(date.today())
    print('Bounce WATCHING list |', date.today(), bounce_watch_list)
    print('Impulse pullback WATCHING list |', date.today(), ip_watch_list)
    print('Bounce ENTER list |', date.today(), bounce_enter_list)
