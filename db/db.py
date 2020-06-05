from contextlib import contextmanager
from psycopg2 import Error, pool
from psycopg2.extras import execute_values

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
            insert_query = 'insert into stock.stock_symbol (symbol) values %s'
            execute_values(cursor, insert_query, stock_list)
            cursor.close()
            conn.commit()
        except Error as error:
            conn.rollback()
            print(error)
