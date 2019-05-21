from copy import deepcopy
from application import app
from resources_tests import BaseTestCase


class TestApiResources(BaseTestCase):

    def test_demo(self):
        resp = app.test_client.get(
            f'/', gather_request=False)
        self.assertEqual(resp.status, 200)
