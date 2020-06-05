from crawler import DataCrawler
from db import db
import json


def load_stock_list(exchange):
    with open('./crawler/stock_list.json') as json_file:
        data = json.load(json_file)
        return data[str.lower(exchange)]


def crawl():
    for stock in load_stock_list('hose'):
        crawler = DataCrawler.DataCrawler(stock, start_date='03/06/2020', end_date='03/06/2020')
        data = crawler.crawl()
        print(data)


def daily_crawl_job():
    crawl()


if __name__ == '__main__':
    # crawl()
    stock_list = load_stock_list('hose')
    stock_list_tuple = [tuple(stock.split()) for stock in sorted(stock_list)]
    print(stock_list_tuple)

    # db.save_stock_list(stock_list_tuple)
