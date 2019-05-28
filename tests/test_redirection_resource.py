from application import app
from tests import BaseTestCase, get_test_query_result
from .mock_for_tests import TEST_USER_URL
from core_api.config import URLS_TABLE


class TestRedirectResource(BaseTestCase):

    def test_redirect_success(self):
        slug = TEST_USER_URL["slug"]
        response = app.test_client.get(f'/{slug}', headers={}, gather_request=False)
        query = f"SELECT clicks from {URLS_TABLE} WHERE slug = '{slug}'"
        query_result = get_test_query_result(query)
        clicks = query_result[0][0]
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url), TEST_USER_URL["url"])
        self.assertEqual(clicks, 5)
