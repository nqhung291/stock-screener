import re
from datetime import datetime

URL_VNDIRECT = 'https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/lich-su-gia.shtml'
API_VNDIRECT = 'https://finfo-api.vndirect.com.vn/v4/stock_prices/'
HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}
API_HEADERS = {'content-type': 'application/json', 'User-Agent': 'Mozilla'}
DATE_FORMAT = '%Y-%m-%d'


def clean_text(text):
    return re.sub('[(\n\t)*]', '', text).strip()


def convert_date(date_string, date_format='%d/%m/%Y'):
    try:
        date_formatted = datetime.strptime(date_string, date_format)
    except ValueError:
        date_formatted = ''
    return date_formatted


def transform_api_to_db(list_data):
    mapped_data = []
    for data in list_data:
        mapped_data.append({
            'symbol': data['code'],
            'date': data['date'],
            'change_amount': float(data['change']),
            'change_percent': float(data['pctChange']),
            'open': float(data['open']),
            'high': float(data['high']),
            'low': float(data['low']),
            'close': float(data['close']),
            'avg': float(data['average']),
            'adjust': float(data['adClose']),
            'volume_match': float(data['nmVolume']),
            'volume_reconcile': float(data['ptVolume'])
        })
    return mapped_data if len(mapped_data) > 0 else None
