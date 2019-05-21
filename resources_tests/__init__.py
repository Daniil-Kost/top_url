import psycopg2
import unittest
import contextvars

from application import create_api
from db_setup import setup
from core_api.config import test_db_conn


class BaseTestCase(unittest.TestCase):

    create_api()
    db = contextvars.ContextVar("db_context")

    def add_test_db_to_ctx(self):
        self.db.set("test_context")

    def add_default_db_to_ctx(self):
        self.db.set("default_context")

    def setUp(self):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute('CREATE DATABASE test')
        conn.close()
        self.add_test_db_to_ctx()
        setup(db_connection=test_db_conn)
        print("!"*50)
        print("Test DB successfully created!")

    def tearDown(self):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute('DROP DATABASE test')
        conn.close()
        self.add_default_db_to_ctx()
        print("!"*50)
        print("Test DB successfully deleted!")

