import requests
from datetime import datetime, date
from crawler import utils
from db import db


def crawl_index(index, start_date, end_date):
    query = "code:{}~date:gte:{}~date:lte:{}".format(index, start_date, end_date)
    delta = datetime.strptime(end_date, utils.DATE_FORMAT) - datetime.strptime(start_date, utils.DATE_FORMAT)
    params = {
        "sort": "date:asc",
        "size": delta.days + 1,
        "page": 1,
        "q": query
    }
    res = requests.get(utils.API_VNDIRECT + '/vnmarket_prices', params=params)
    data = res.json()['data']
    data_formated = utils.transform_index_api_to_db(data)
    db.insert_index_price(data_formated)


def crawl_all_index(start_date, end_date=date.today().strftime(utils.DATE_FORMAT)):
    index_list = db.get_index_symbol()
    for index in index_list:
        crawl_index(index, start_date, end_date)
