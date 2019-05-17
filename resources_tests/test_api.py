from unittest import TestCase
from copy import deepcopy
import unittest
from core_api.config import db_conn, test_db_conn
from application import app, create_api
import os



class TestApiResources(TestCase):

    create_api()

    def test_get_urls(self):

        req, resp = app.test_client.get(
            f'/')
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(__name__)
        self.assertEqual(resp.status, 200)


if __name__ == "__main__":
    unittest.main()
