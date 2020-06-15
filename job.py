from crawler import DataCrawler
from db import db
import json


def load_stock_list(exchange):
    with open('./crawler/stock_list.json') as json_file:
        data = json.load(json_file)
        return data[str.lower(exchange)]


def save_stock_list():
    stock_list = load_stock_list('hose')
    stock_list_tuple = [tuple(stock.split()) for stock in sorted(stock_list)]
    print(stock_list_tuple)
    db.save_stock_list(stock_list_tuple)


def crawl():
    for stock in db.get_stock_symbol():
        crawler = DataCrawler.DataCrawler(stock, start_date='05/06/2020')
        data = crawler.crawl()
        if data is not None:
            db.insert_stock_price(data)
        print('done crawl', stock)


def crawl_one_stock():
    crawler = DataCrawler.DataCrawler('VCB', start_date='11/06/2020', end_date='12/06/2020')
    data = crawler.crawl()
    if data is not None:
        db.insert_stock_price(data)
    print(data)


if __name__ == '__main__':
    crawl_one_stock()
