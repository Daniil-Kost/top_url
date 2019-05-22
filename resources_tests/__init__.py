import psycopg2
import unittest
import contextvars
import asyncio

from application import create_api
from db_setup import setup
from core_api.config import test_db_conn, URLS_TABLE, USER_TABLE, USER_URLS_TABLE
from .fixtures import ALL_URLS_DATA, USER_DATA, USER_URLS_DATA, TEST_USER_URLS


async def load_fixtures():
    # Load urls data
    for data in ALL_URLS_DATA:
        await test_db_conn.insert(URLS_TABLE, tuple(data.values()), tuple(data.keys()))
    # Load user data
    await test_db_conn.insert(USER_TABLE, tuple(USER_DATA.values()), tuple(USER_DATA.keys()))
    # Load user urls data
    await test_db_conn.insert(USER_URLS_TABLE, tuple(USER_URLS_DATA.values()), tuple(USER_URLS_DATA.keys()))


class BaseTestCase(unittest.TestCase):

    create_api()
    db_context = contextvars.ContextVar("db_context")

    headers = {"Authorization": f"Token {USER_DATA['token']}", "Content-Type": "application/json"}

    def _add_test_db_to_ctx(self):
        self.db_context.set("test_context")

    def _add_default_db_to_ctx(self):
        self.db_context.set("default_context")

    def setUp(self):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute('CREATE DATABASE urls_test')
        conn.close()
        print("!"*50)
        print("Test DB successfully created!")
        self._add_test_db_to_ctx()
        setup(db_connection=test_db_conn)
        asyncio.run(load_fixtures())

    def tearDown(self):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute('DROP DATABASE IF EXISTS urls_test')
        conn.close()
        print("!"*50)
        print("Test DB successfully deleted!")
        self._add_default_db_to_ctx()

