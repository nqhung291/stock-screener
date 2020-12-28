from abc import ABC, abstractmethod
from crawler import utils
import requests
from datetime import date, datetime


class DataCrawler:
    def __init__(self,
                 symbols,
                 start_date=date.today().strftime("%d/%m/%Y"),
                 end_date=date.today().strftime("%d/%m/%Y"),
                 data_source='VNDIRECT',
                 *args, **kwargs):
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date
        self.data_source = data_source

    def crawl(self):
        if self.data_source == 'VNDIRECT':
            crawler = VndirectAPILoader(self.symbols, self.start_date, self.end_date)
            return crawler.crawl()


class BaseDataLoader(ABC):
    def __init__(self, symbols, start_date, end_date, *args, **kwargs):
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date

    @abstractmethod
    def crawl(self):
        pass


class VndirectAPILoader(BaseDataLoader):
    def __init__(self, symbols, start_date, end_date, *args, **kwargs):
        super().__init__(symbols, start_date, end_date)

    def crawl(self):
        price_data = []
        if not isinstance(self.symbols, list):
            symbols = [self.symbols]
        else:
            symbols = self.symbols

        for symbol in symbols:
            price_data = self.crawl_one_symbol(str.upper(symbol))
        return price_data

    def crawl_one_symbol(self, symbol):
        query = 'code:' + symbol + '~date:gte:' + self.start_date + '~date:lte:' + self.end_date
        delta = datetime.strptime(self.end_date, utils.DATE_FORMAT) - datetime.strptime(self.start_date, utils.DATE_FORMAT)
        params = {
            "sort": "date",
            "size": delta.days + 1,
            "page": 1,
            "q": query
        }
        res = requests.get(utils.API_VNDIRECT, params=params)
        data = res.json()['data']
        return utils.transform_api_to_db(data)





