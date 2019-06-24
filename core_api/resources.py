import psycopg2
from lemkpg.constants import GET_ALL_COLUMNS as ALL_COLUMNS
from sanic.views import HTTPMethodView
from sanic import response
from http import HTTPStatus
from jinja2 import Environment, PackageLoader, select_autoescape

from .forms import CreateNewShortUrlForm, UserRegistrationForm, UserAuthForm
from .config import (
    URLS_TABLE,
    USER_TABLE,
    USER_URLS_TABLE,
    URLS_COLUMNS
)
from .utils import (
    response_converter,
    prepare_post_url_data,
    prepare_user_registration_data,
    check_username_existing,
    get_url_by_uuid,
    get_user_urls,
)


class UrlsView(HTTPMethodView):

    async def get(self, request):
        db_conn = request["db_conn"]
        query_result = await get_user_urls(db_conn, request["user"]["id"])
        exclude_fields = ("id", "domain", "slug")
        result = response_converter(query_result, URLS_COLUMNS, exclude_fields)
        return response.json(result)

    async def post(self, request):
        db_conn = request["db_conn"]
        form_data, errors = CreateNewShortUrlForm().load(request.json)
        if errors:
            return response.json(errors, HTTPStatus.BAD_REQUEST)
        data = prepare_post_url_data(form_data)

        try:
            await db_conn.insert(URLS_TABLE, tuple(data.values()), tuple(data.keys()))
        except psycopg2.ProgrammingError as e:
            return response.json({"error": e}, HTTPStatus.BAD_REQUEST)

        try:
            query_result = await db_conn.get(URLS_TABLE, ALL_COLUMNS,
                                             conditions_list=[("uuid", "=", data["uuid"], None)])
            await db_conn.insert(USER_URLS_TABLE, (request["user"]["id"],
                                                   query_result[0][0]), ("user_id", "url_id"))
            exclude_fields = ("id", "domain", "slug")
            result = response_converter(query_result, URLS_COLUMNS, exclude_fields)
            return response.json(result[0], HTTPStatus.CREATED)
        except psycopg2.ProgrammingError as e:
            return response.json({"error": e}, HTTPStatus.INTERNAL_SERVER_ERROR)


class UrlView(HTTPMethodView):

    async def get(self, request, url_uuid):
        db_conn = request["db_conn"]
        query_result = await get_url_by_uuid(db_conn, url_uuid, request["user"]["id"])
        if not query_result:
            return response.json({"error": "This url not found for this user"}, HTTPStatus.NOT_FOUND)
        exclude_fields = ("id", "domain", "slug")
        result = response_converter(query_result, URLS_COLUMNS, exclude_fields)
        return response.json(result[0])

    async def delete(self, request, url_uuid):
        db_conn = request["db_conn"]
        query_result = await get_url_by_uuid(db_conn, url_uuid, request["user"]["id"])
        if not query_result:
            return response.json({"error": "This url not found for this user"}, HTTPStatus.NOT_FOUND)
        await db_conn.delete_records(URLS_TABLE, conditions_list=[("uuid", "=", url_uuid, None)])
        return response.json({}, HTTPStatus.NO_CONTENT)


class RegisterView(HTTPMethodView):

    async def post(self, request):
        db_conn = request["db_conn"]
        form_data, errors = UserRegistrationForm().load(request.json)
        if errors:
            return response.json(errors, HTTPStatus.BAD_REQUEST)
        if await check_username_existing(db_conn, form_data["username"]):
            return response.json({"error": "User with this username already exists"}, HTTPStatus.CONFLICT)
        data = prepare_user_registration_data(form_data)
        try:
            await db_conn.insert(USER_TABLE, tuple(data.values()), tuple(data.keys()))
        except psycopg2.ProgrammingError as e:
            return response.json({"error": e}, HTTPStatus.BAD_REQUEST)

        query_result = await db_conn.get(USER_TABLE, ["id", "token"],
                                         conditions_list=[("uuid", "=", data["uuid"], None)])
        result = {"token": query_result[0][1]}
        return response.json(result, HTTPStatus.CREATED)


class AuthView(HTTPMethodView):

    async def post(self, request):
        db_conn = request["db_conn"]
        form_data, errors = UserAuthForm().load(request.json)
        if errors:
            return response.json(errors, HTTPStatus.BAD_REQUEST)
        query_result = await db_conn.get(USER_TABLE, ["token"],
                                         conditions_list=[("username", "=", form_data["username"], None),
                                                          ("password", "=", form_data["password"], "AND")])
        result = {"token": query_result[0][0]}
        return response.json(result)


class RedirectView(HTTPMethodView):

    async def get(self, request, slug):
        db_conn = request["db_conn"]
        query_result = await db_conn.get(URLS_TABLE, ALL_COLUMNS, conditions_list=[("slug", "=", slug, None)])
        url_for_redirect = query_result[0][2]
        url_uuid = query_result[0][1]
        short_url_clicks = query_result[0][7] + 1
        await db_conn.update(URLS_TABLE, {"clicks": short_url_clicks}, [("uuid", "=", url_uuid, None)])
        return response.redirect(url_for_redirect)


class DemoResource(HTTPMethodView):

    async def get(self, request):
        env = Environment(
            loader=PackageLoader('application', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('index.html')
        return response.html(template.render(request=request, user=request["user"]))