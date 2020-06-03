from abc import ABC, abstractmethod
from crawler import utils
from bs4 import BeautifulSoup
import requests
from datetime import date


class DataCrawler:
    def __init__(self,
                 symbols,
                 start_date=date.today().strftime("%d/%m/%Y"),
                 end_date=date.today().strftime("%d/%m/%Y"),
                 data_source='VNDIRECT',
                 *args, **kwargs):
        self.symbol = symbols
        self.start_date = start_date
        self.end_date = end_date
        self.data_source = data_source

    def crawl(self):
        if self.data_source == 'VNDIRECT':
            crawler = VndirectDataLoader(self.symbol, self.start_date, self.end_date)
            crawler.crawl()


class BaseDataLoader(ABC):
    def __init__(self, symbols, start_date, end_date, *args, **kwargs):
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date

    @abstractmethod
    def crawl(self):
        pass


class VndirectDataLoader(BaseDataLoader):
    def __init__(self, symbols, start_date, end_date, *args, **kwargs):
        super().__init__(symbols, start_date, end_date)

    def crawl(self):
        if not isinstance(self.symbols, list):
            symbols = [self.symbols]
        else:
            symbols = self.symbols

        for symbol in symbols:
            self.crawl_one_symbol(str.upper(symbol))

    def crawl_one_symbol(self, symbol):
        last_page = self.get_last_page(symbol)
        for i in range(last_page):
            self.crawl_one_symbol_by_page(symbol, i + 1)

    def crawl_one_symbol_by_page(self, symbol, page):
        form_data = {
            "model.downloadType": "",
            "pagingInfo.indexPage": str(page),
            "searchMarketStatisticsView.symbol": symbol,
            "strFromDate": self.start_date,
            "strToDate": self.end_date
        }
        r = requests.post(utils.URL_VNDIRECT, form_data, utils.HEADERS)
        soup = BeautifulSoup(r.content, 'html.parser')
        data = soup.find(class_='list_tktt lichsugia')

        history_data = []

        for i, li_tag in enumerate(data.find_all('li')):
            if not li_tag.has_attr('class'):
                info = {}
                for j, value in enumerate(li_tag.select('div')):
                    value = utils.clean_text(value.text)
                    if j == 0:
                        info['date'] = value
                    if j == 1:
                        values = value.split()
                        info['change_amount'] = values[0]
                        info['change_percent'] = values[1]
                    if j == 2:
                        info['open'] = value
                    if j == 3:
                        info['high'] = value
                    if j == 4:
                        info['low'] = value
                    if j == 5:
                        info['close'] = value
                    if j == 6:
                        info['avg'] = value
                    if j == 7:
                        info['adjust'] = value
                    if j == 8:
                        info['volume_match'] = value
                    if j == 9:
                        info['volume_reconcile'] = value
                history_data.append(info)
        print(history_data)

    def get_last_page(self, symbol):
        form_data = {
            "model.downloadType": "",
            "pagingInfo.indexPage": "",
            "searchMarketStatisticsView.symbol": symbol,
            "strFromDate": self.start_date,
            "strToDate": self.end_date
        }
        r = requests.post(utils.URL_VNDIRECT, form_data, headers=utils.HEADERS)
        soup = BeautifulSoup(r.content, 'html.parser')
        text_div = soup.find('div', class_='paging').get_text()
        try:
            last_page = int(text_div.split()[1].split('/')[1])
        except IndexError:
            last_page = int(text_div)
        return last_page




