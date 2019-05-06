import psycopg2
from lemkpg.constants import GET_ALL_COLUMNS as ALL_COLUMNS, ID
from sanic.views import HTTPMethodView
from sanic import response
from http import HTTPStatus

from .utils import response_converter, prepare_post_url_data
from .config import URLS_TABLE, PROFILE_TABLE, URLS_COLUMNS, PROFILE_COLUMNS, db_conn


class UrlsView(HTTPMethodView):

    async def get(self, request):
        query_result = await db_conn.get_all(URLS_TABLE)
        exclude_fields = ("id", "domain", "slug")
        result = response_converter(query_result, URLS_COLUMNS, exclude_fields)
        return response.json(result)

    async def post(self, request):
        form_data, _ = CreateNewShortUrlForm().load(request.json)
        data = prepare_post_url_data(form_data)
        try:
            await db_conn.insert(URLS_TABLE, tuple(data.values()),
                                 ("uuid", "url", "title", "domain", "short_url", "slug", "clicks", "create_dttm"))
        except psycopg2.ProgrammingError as e:
            print(e)
            return response.json({"error": e}, HTTPStatus.BAD_REQUEST)

        query_result = await db_conn.get(URLS_TABLE, ALL_COLUMNS, conditions_list=[("uuid", "=", data["uuid"], None)])
        exclude_fields = ("id", "domain", "slug")
        result = response_converter(query_result, URLS_COLUMNS, exclude_fields)
        return response.json(result[0], HTTPStatus.CREATED)


class NewView(HTTPMethodView):

    async def get(self, request):
        query_result = await db_conn.full_join(
            URLS_TABLE, PROFILE_TABLE, (f"{URLS_TABLE}.{ID}", "=", f"{PROFILE_TABLE}.{ID}"))
        columns = URLS_COLUMNS + PROFILE_COLUMNS
        exclude_fields = ("id", "domain", "slug")
        result = response_converter(query_result, columns, exclude_fields)
        return response.json(result)
