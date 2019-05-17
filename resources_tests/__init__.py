import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def demo():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    with conn.cursor() as cur:
        cur.execute('CREATE DATABASE demo_test')

    conn.close()
