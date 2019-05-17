from unittest import TestCase
from copy import deepcopy
import unittest
from core_api.config import db_conn, test_db_conn
from application import app, create_api
import os
import contextvars
from resources_tests import demo

class TestApiResources(TestCase):

    create_api()
    db = contextvars.ContextVar("db")

    def add_test_db_ctx(self):
        self.db.set("test_context")

    def add_default_db_ctx(self):
        self.db.set("default_context")

    def test_demo(self):
        demo()
        self.add_test_db_ctx()
        resp = app.test_client.get(
            f'/', gather_request=False)
        self.assertEqual(resp.status, 200)
        self.add_default_db_ctx()


if __name__ == "__main__":
    unittest.main()
