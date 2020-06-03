from crawler import DataCrawler
import json


def load_stock_list(exchange):
    with open('stock_list.json') as json_file:
        data = json.load(json_file)
        return data[str.lower(exchange)]


def main():
    for stock in load_stock_list('hose'):
        crawler = DataCrawler.DataCrawler(stock).crawl()


if __name__ == '__main__':
    main()
