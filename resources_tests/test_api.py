import json
from copy import deepcopy

from application import app
from resources_tests import BaseTestCase
from .mock_for_tests import (
    TEST_USER_URL,
    URL_POST_DATA,
    URL_VALIDATION_ERROR,
    SHORT_URL_VALIDATION_ERROR,
    URL_POST_DATA_WITH_VALID_SHORT_URL,
    URL_POST_DATA_WITH_INVALID_SHORT_URL,
    ANOTHER_USER_URL,
    NOT_FOUND_URL_ERROR,
)


class TestApiResources(BaseTestCase):

    def test_get_urls_success(self):
        correct_json_output = deepcopy(TEST_USER_URL)
        correct_json_output.pop("domain")
        correct_json_output.pop("slug")

        response = app.test_client.get(
            '/api/v1/urls', headers=self.headers, gather_request=False)

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json[0], correct_json_output)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(type(response.json), list)

    def test_get_urls_failed_without_token(self):
        response = app.test_client.get(
            '/api/v1/urls', headers={}, gather_request=False)

        self.assertEqual(response.status, 401)
        self.assertEqual(response.text, 'Error: Authorization should be defined in request headers')

    def test_get_urls_failed_with_invalid_token(self):
        response = app.test_client.get(
            '/api/v1/urls', headers={"Authorization": f"Token 844895y45yrrtgrgrgree"}, gather_request=False)

        self.assertEqual(response.status, 401)
        self.assertEqual(response.text, 'Error: Authorization with valid Token should be defined in request headers')

    def test_post_url_success(self):
        data = json.dumps(URL_POST_DATA)
        response = app.test_client.post(
            '/api/v1/urls', headers=self.headers, data=data, gather_request=False)

        self.assertEqual(response.status, 201)
        self.assertEqual(type(response.json), dict)
        self.assertIn("short_url", response.json)
        self.assertIn("uuid", response.json)
        self.assertEqual(response.json["clicks"], 0)
        self.assertEqual(response.json["url"], URL_POST_DATA["url"])

    def test_post_url_failed_with_unauthorized(self):
        data = json.dumps(URL_POST_DATA)
        response = app.test_client.post(
            '/api/v1/urls', headers={}, data=data, gather_request=False)

        self.assertEqual(response.status, 401)
        self.assertEqual(response.text, 'Error: Authorization should be defined in request headers')

    def test_post_url_failed_with_url_validation_error(self):
        data = json.dumps({})
        response = app.test_client.post(
            '/api/v1/urls', headers=self.headers, data=data, gather_request=False)

        self.assertEqual(response.status, 400)
        self.assertEqual(response.json, URL_VALIDATION_ERROR)

    def test_post_url_success_with_custom_short_url(self):
        data = json.dumps(URL_POST_DATA_WITH_VALID_SHORT_URL)
        response = app.test_client.post(
            '/api/v1/urls', headers=self.headers, data=data, gather_request=False)

        self.assertEqual(response.status, 201)
        self.assertEqual(type(response.json), dict)
        self.assertIn("short_url", response.json)
        self.assertIn("uuid", response.json)
        self.assertEqual(response.json["clicks"], 0)
        self.assertEqual(response.json["url"], URL_POST_DATA["url"])
        self.assertIn(URL_POST_DATA_WITH_VALID_SHORT_URL["short_url"], response.json["short_url"])

    def test_post_url_failed_with_short_url_validation_error(self):
        data = json.dumps(URL_POST_DATA_WITH_INVALID_SHORT_URL)
        response = app.test_client.post(
            '/api/v1/urls', headers=self.headers, data=data, gather_request=False)

        self.assertEqual(response.status, 400)
        self.assertEqual(response.json, SHORT_URL_VALIDATION_ERROR)

    def test_get_url_by_uuid_success(self):
        correct_json_output = deepcopy(TEST_USER_URL)
        correct_json_output.pop("domain")
        correct_json_output.pop("slug")
        uuid = TEST_USER_URL["uuid"]

        response = app.test_client.get(
            f'/api/v1/urls/{uuid}', headers=self.headers, gather_request=False)

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, correct_json_output)
        self.assertEqual(response.json["uuid"], uuid)
        self.assertIn("short_url", response.json)

    def test_get_url_by_uuid_failed_because_url_not_in_user_urls(self):
        uuid = ANOTHER_USER_URL["uuid"]
        response = app.test_client.get(
            f'/api/v1/urls/{uuid}', headers=self.headers, gather_request=False)

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, NOT_FOUND_URL_ERROR)

    def test_get_url_by_uuid_failed_with_unauthorized(self):
        uuid = TEST_USER_URL["uuid"]
        response = app.test_client.get(
            f'/api/v1/urls/{uuid}', headers={}, gather_request=False)

        self.assertEqual(response.status, 401)
        self.assertEqual(response.text, 'Error: Authorization should be defined in request headers')

    def test_delete_url_success(self):
        uuid = TEST_USER_URL["uuid"]
        response = app.test_client.delete(
            f'/api/v1/urls/{uuid}', headers=self.headers, gather_request=False)

        get_response = app.test_client.get(
            f'/api/v1/urls/{uuid}', headers=self.headers, gather_request=False)

        self.assertEqual(response.status, 204)
        self.assertEqual(get_response.status, 404)
        self.assertEqual(get_response.json, NOT_FOUND_URL_ERROR)

    def test_delete_url_failed_because_url_not_in_user_urls(self):
        uuid = ANOTHER_USER_URL["uuid"]
        response = app.test_client.delete(
            f'/api/v1/urls/{uuid}', headers=self.headers, gather_request=False)

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, NOT_FOUND_URL_ERROR)

    def test_delete_url_by_uuid_failed_with_unauthorized(self):
        uuid = TEST_USER_URL["uuid"]
        response = app.test_client.delete(
            f'/api/v1/urls/{uuid}', headers={}, gather_request=False)

        self.assertEqual(response.status, 401)
        self.assertEqual(response.text, 'Error: Authorization should be defined in request headers')


