from crawler import DataCrawler
from crawler.index_crawler import crawl_all_index
from db import db
import json
from datetime import date
import datetime
from crawler import utils
from utils.helpers import get_screen_result
import requests


def load_stock_list(exchange):
    with open('./crawler/stock_list.json') as json_file:
        data = json.load(json_file)
        return data[str.lower(exchange)]


def save_stock_list():
    exchange = 'HNX'
    stock_list = load_stock_list(exchange)
    stock_list_tuple = [(stock, exchange) for stock in sorted(stock_list)]
    db.save_stock_list(stock_list_tuple)


def crawl_one_symbol(stock, exchange, start_date, end_date):
    crawler = DataCrawler.DataCrawler(stock, start_date=start_date, end_date=end_date)
    data = crawler.crawl()
    if data is not None:
        db.insert_stock_price(data)
        print('done crawl', exchange + ':', stock, 'from:', start_date, 'to:', end_date)
    else:
        print('ERROR crawl', exchange + ':', stock, 'from:', start_date, 'to:', end_date)


def crawl(exchange=None,
          start_date=date.today().strftime(utils.DATE_FORMAT),
          end_date=date.today().strftime(utils.DATE_FORMAT)
          ):
    for (stock, exchange) in db.get_stock_symbol(exchange):
        crawl_one_symbol(stock, exchange, start_date, end_date)


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
            crawl_all_index(start_date=start_date, end_date=end_date.strftime(utils.DATE_FORMAT))
    elif latest_date < date.today() - datetime.timedelta(days=1) or \
            (latest_date == date.today() - datetime.timedelta(days=1) and datetime.datetime.today().hour > 16):
        start_date = (latest_date + datetime.timedelta(days=1)).strftime(utils.DATE_FORMAT)
        crawl(start_date=start_date, end_date=end_date.strftime(utils.DATE_FORMAT))
        crawl_all_index(start_date=start_date, end_date=end_date.strftime(utils.DATE_FORMAT))
    get_screen_result(date.today() - datetime.timedelta(days=10), date.today())


def run_custom_crawl(start_date, end_date):
    crawl(start_date=start_date, end_date=end_date)


def run_crawl_to_min_date(start_date):
    for (stock, exchange) in db.get_stock_symbol():
        end_date = db.get_min_symbol_date(stock) - datetime.timedelta(days=1)
        end_date_str = date.strftime(end_date, utils.DATE_FORMAT)
        if start_date > end_date_str:
            continue
        crawl_one_symbol(stock, exchange, start_date, end_date_str)


def insert_stock_info():
    for (symbol, _) in db.get_stock_symbol():
        params_string = 'code:{symbol}'.format(symbol=symbol)
        params_dict = {
            'q': params_string
        }
        response = requests.get('https://finfo-api.vndirect.com.vn/v4/company_profiles', params=params_dict)
        data = response.json()['data']
        db.insert_stock_info(symbol, data[0])


if __name__ == '__main__':
    run_daily_crawl()
    # run_custom_crawl('2010-01-01', '2021-05-06')
    # run_crawl_to_min_date('2014-02-01')
    # insert_stock_info()
