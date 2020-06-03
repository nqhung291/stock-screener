from crawler import DataCrawler
from pymongo import MongoClient
import json

MONGO_URL = '172.17.0.2:27017'


def load_stock_list(exchange):
    with open('./crawler/stock_list.json') as json_file:
        data = json.load(json_file)
        return data[str.lower(exchange)]


def main():
    client = MongoClient(MONGO_URL)
    db = client.stock
    for stock in load_stock_list('hose'):
        crawler = DataCrawler.DataCrawler(stock, start_date='01/06/2019')
        data = crawler.crawl()
        print(data)
        db.stock_price.insert_one({
            'symbol': stock,
            'prices': data
        })


if __name__ == '__main__':
    main()
