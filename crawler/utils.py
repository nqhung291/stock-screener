import re
from datetime import datetime

URL_VNDIRECT = 'https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/lich-su-gia.shtml'
HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}


def clean_text(text):
    return re.sub('[(\n\t)*]', '', text).strip()


def convert_date(date_string, date_format='%d/%m/%Y'):
    try:
        date_formatted = datetime.strptime(date_string, date_format)
    except ValueError:
        date_formatted = ''
    return date_formatted
