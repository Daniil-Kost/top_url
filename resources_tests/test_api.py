from copy import deepcopy

from application import app
from resources_tests import BaseTestCase
from .fixtures import TEST_USER_URLS


class TestApiResources(BaseTestCase):

    def test_urls_resource_success(self):
        correct_json_output = deepcopy(TEST_USER_URLS)
        correct_json_output.pop("domain")
        correct_json_output.pop("slug")
        response = app.test_client.get(
            f'/api/v1/urls', headers=self.headers, gather_request=False)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json[0], correct_json_output)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(type(response.json), list)
