import psycopg2
from lemkpg.constants import GET_ALL_COLUMNS as ALL_COLUMNS, ID
from sanic.views import HTTPMethodView
from sanic import response
from http import HTTPStatus

from .config import URLS_TABLE, USER_TABLE, URLS_COLUMNS, USER_COLUMNS, db_conn
from .forms import CreateNewShortUrlForm, UserRegistrationForm, UserAuthForm
from .utils import (
    response_converter,
    prepare_post_url_data,
    prepare_user_register_data,
    check_username_existing,)


class UrlsView(HTTPMethodView):

    async def get(self, request):
        query_result = await db_conn.get_all(URLS_TABLE)
        exclude_fields = ("id", "domain", "slug")
        result = response_converter(query_result, URLS_COLUMNS, exclude_fields)
        return response.json(result)

    async def post(self, request):
        form_data, errors = CreateNewShortUrlForm().load(request.json)
        if errors:
            return response.json(errors, HTTPStatus.BAD_REQUEST)
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


class UrlView(HTTPMethodView):

    async def get(self, request, url_uuid):
        query_result = await db_conn.get(URLS_TABLE, ALL_COLUMNS, conditions_list=[("uuid", "=", url_uuid, None)])
        exclude_fields = ("id", "domain", "slug")
        result = response_converter(query_result, URLS_COLUMNS, exclude_fields)
        return response.json(result[0])

    async def delete(self, request, url_uuid):
        await db_conn.delete_records(URLS_TABLE, conditions_list=[("uuid", "=", url_uuid, None)])
        return response.json({}, HTTPStatus.NO_CONTENT)


class RegisterView(HTTPMethodView):

    async def post(self, request):
        form_data, errors = UserRegistrationForm().load(request.json)
        if errors:
            return response.json(errors, HTTPStatus.BAD_REQUEST)
        if await check_username_existing(form_data["username"]):
            return response.json({"error": "User with this username already exist"}, HTTPStatus.CONFLICT)
        data = prepare_user_register_data(form_data)
        try:
            await db_conn.insert(USER_TABLE, tuple(data.values()),
                                 ("uuid", "username", "password", "token"))
        except psycopg2.ProgrammingError as e:
            print(e)
            return response.json({"error": e}, HTTPStatus.BAD_REQUEST)

        query_result = await db_conn.get(USER_TABLE, ["token"], conditions_list=[("uuid", "=", data["uuid"], None)])
        result = {"token": query_result[0][0]}
        return response.json(result, HTTPStatus.CREATED)
