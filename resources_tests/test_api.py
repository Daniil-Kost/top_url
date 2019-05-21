from copy import deepcopy
from application import app
from resources_tests import BaseTestCase


class TestApiResources(BaseTestCase):

    def test_urls_resource_success(self):
        resp = app.test_client.get(
            f'/api/v1/urls', gather_request=False)
        self.assertEqual(resp.status, 200)
