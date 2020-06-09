from crawler import DataCrawler
from db import db
from analysis import ta
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
    for stock in load_stock_list('hose'):
        crawler = DataCrawler.DataCrawler(stock, start_date='05/06/2019', end_date='04/06/2020')
        data = crawler.crawl()
        db.insert_stock_price(data)


if __name__ == '__main__':
    # stock_data = db.get_stock_price('VCB')
    #
    # open = np.asarray([i[0] for i in stock_data])
    # high = np.asarray([i[1] for i in stock_data])
    # low = np.asarray([i[2] for i in stock_data])
    # close = np.asarray([i[3] for i in stock_data])
    #
    # doji = abstract.CDLENGULFING(open, high, low, close).tolist()
    # dojidate = [(i, stock_data[index][5]) for index, i in enumerate(doji) if i != 0]
    # print(dojidate)
    # result1 = abstract.EMA(close, timeperiod=18)
    # result2 = abstract.EMA(close, timeperiod=50)
    # result3 = abstract.EMA(close, timeperiod=100)
    # result4 = abstract.EMA(close, timeperiod=150)
    # print(result1)
    # print(result2)
    # print(result3)
    # print(result4)
    # print(db.pd_get_stock('VCB'))
    ta.bounce_strategy_backtest()


