from contextlib import contextmanager
from psycopg2 import Error, pool
from psycopg2.extras import execute_batch, execute_values
from datetime import datetime, timedelta

POSTGRES_HOST = '172.17.0.2'
POSTGRES_PORT = '5432'
POSTGRES_DB = 'stock'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'pass'

db_pool = pool.SimpleConnectionPool(minconn=1,
                                    maxconn=10,
                                    host=POSTGRES_HOST,
                                    database=POSTGRES_DB,
                                    user=POSTGRES_USER,
                                    password=POSTGRES_PASSWORD,
                                    port=POSTGRES_PORT)


@contextmanager
def connect_db():
    conn = db_pool.getconn()
    cursor = conn.cursor()
    try:
        yield conn, cursor
    finally:
        cursor.close()
        db_pool.putconn(conn)


def save_stock_list(stock_list):
    with connect_db() as (conn, cursor):
        try:
            insert_query = 'insert into stock.stock.stock_symbol (symbol, exchange) values %s'
            execute_values(cursor, insert_query, stock_list)
            cursor.close()
            conn.commit()
        except Error as error:
            conn.rollback()
            print(error)


def insert_stock_price(stock_price_list):
    with connect_db() as (conn, cursor):
        try:
            insert_query = 'insert into stock.stock.stock_price (' \
                           'symbol_id, date, change_amount, change_percent, ' \
                           'open, high, low, close, avg, adjust, ' \
                           'volume_match, volume_reconcile' \
                           ') values (' \
                           '(select id from stock.stock.stock_symbol where symbol = %(symbol)s),' \
                           '%(date)s, %(change_amount)s, %(change_percent)s, %(open)s, %(high)s, %(low)s, ' \
                           '%(close)s, %(avg)s, %(adjust)s, %(volume_match)s, %(volume_reconcile)s' \
                           ') on conflict on constraint symbol_id_date_unique do nothing'

            execute_batch(cursor, insert_query, stock_price_list)
            cursor.close()
            conn.commit()
        except Error as error:
            conn.rollback()
            print(error)


def get_stock_symbol(exchange=None):
    with connect_db() as (conn, cursor):
        try:
            if exchange is None:
                query = 'select symbol, exchange from stock.stock.stock_symbol'
                cursor.execute(query)
            else:
                query = 'select symbol, exchange from stock.stock.stock_symbol where exchange in %(list_exchange)s'
                if not isinstance(exchange, list):
                    exchange = list(exchange.split())
                cursor.execute(query, {
                    'list_exchange': tuple(exchange)
                })
            # iterate through result set
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                yield row
        except Error as error:
            print(error)


def get_price(symbol, end_date=datetime.today()):
    initial_date = (end_date - timedelta(days=300)).strftime('%Y-%m-%d')
    with connect_db() as (conn, cursor):
        try:
            query = 'select open, high, low, close, to_char(date, \'YYYY-MM-DD\') as date ' \
                    'from stock.stock.stock_price as p ' \
                    'inner join stock.stock.stock_symbol as s on p.symbol_id = s.id ' \
                    'where symbol = \'{symbol}\'' \
                    'and date >= \'{initial_date}\' and date <= \'{end_date}\'  order by date'\
                .format(symbol=symbol, initial_date=initial_date, end_date=end_date.strftime('%Y-%m-%d'))
            cursor.execute(query)
            open = []
            high = []
            low = []
            close = []
            date = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                open.append(row[0])
                high.append(row[1])
                low.append(row[2])
                close.append(row[3])
                date.append(row[4])
            cursor.close()
            return open, high, low, close, date
        except Error as error:
            print(error)


def get_max_date():
    with connect_db() as (conn, cursor):
        try:
            query = 'select max(date) from stock.stock.stock_price'
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            return row[0]
        except Error as error:
            print(error)
