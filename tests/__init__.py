import asyncio
import contextvars
import psycopg2
import unittest

from application import create_api
from db_setup import setup
from core_api.config import (
    test_db_conn,
    URLS_TABLE,
    USER_TABLE,
    USER_URLS_TABLE,
    TEST_CONNECTION_DB_NAME,
    TEST_CONNECTION_DB_PASSWORD,
    TEST_CONNECTION_DB_USER,
    TEST_CONNECTION_DB_HOST,
)
from .fixtures import ALL_URLS_DATA, USER_DATA, USER_URLS_DATA


def get_test_query_result(query):
    async def execute_query():
        query_result = await test_db_conn.raw_query(query)
        return query_result
    result = asyncio.run(execute_query())
    return result


async def load_fixtures():
    # Load urls data
    for data in ALL_URLS_DATA:
        await test_db_conn.insert(URLS_TABLE, tuple(data.values()), tuple(data.keys()))
    # Load user data
    await test_db_conn.insert(USER_TABLE, tuple(USER_DATA.values()), tuple(USER_DATA.keys()))
    # Load user urls data
    await test_db_conn.insert(USER_URLS_TABLE, tuple(USER_URLS_DATA.values()), tuple(USER_URLS_DATA.keys()))
    print("Fixtures successfully loaded!")


class BaseTestCase(unittest.TestCase):

    create_api()
    context = contextvars.ContextVar("db_context")

    headers = {"Authorization": f"Token {USER_DATA['token']}", "Content-Type": "application/json"}

    def _set_test_ctx(self):
        self.context.set("test_context")

    def _set_default_ctx(self):
        self.context.set("default_context")

    def setUp(self):
        conn = psycopg2.connect(dbname=TEST_CONNECTION_DB_NAME, user=TEST_CONNECTION_DB_USER,
                                password=TEST_CONNECTION_DB_PASSWORD, host=TEST_CONNECTION_DB_HOST)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute('CREATE DATABASE urls_test')
        conn.close()
        print("Test DB successfully created!")
        self._set_test_ctx()
        # run setup() func for create all required tables in test db
        setup(db_connection=test_db_conn)
        asyncio.run(load_fixtures())

    def tearDown(self):
        conn = psycopg2.connect(dbname=TEST_CONNECTION_DB_NAME, user=TEST_CONNECTION_DB_USER,
                                password=TEST_CONNECTION_DB_PASSWORD, host=TEST_CONNECTION_DB_HOST)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute('DROP DATABASE IF EXISTS urls_test')
        conn.close()
        print("Test DB successfully deleted!")
        self._set_default_ctx()
