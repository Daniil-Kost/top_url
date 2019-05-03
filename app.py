import uuid
import psycopg2
import shortuuid
from lemkpg import AsyncLemkPgApi
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic import response
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from datetime import datetime
from http import HTTPStatus
from marshmallow.validate import OneOf, Length
from marshmallow import (
    Schema,
    fields,
    post_load,
    validates,
    pre_load
)


DEFAULT_DOMAIN = "http://localhost:8000"
app = Sanic("app")
db_conn = AsyncLemkPgApi(db_name="urls_database", db_password="postgres", db_user="postgres", db_host="localhost")


class CreateNewShortUrlForm(Schema):
    url = fields.Url(required=True)
    short_url = fields.String(required=False, default=None)


def response_converter(query_result, columns, exclude_fields=None):
    result = []
    for records in query_result:
        values = [record for record in records]
        for i, val in enumerate(values):
            if not isinstance(val, (int, float, dict, list, tuple)):
                values[i] = str(val)
        response_data = dict(zip(columns, values))
        if exclude_fields:
            for field in set(exclude_fields):
                response_data.pop(field)
        result.append(response_data)
    return result


# generate random short url
def short_url_generator():
    return f"{shortuuid.uuid()[0:8]}"


# function for getting title in <h1> tag
def get_title(url):
    try:
        html = urlopen(url)
    except HTTPError:
        print("This web-page: " + url + " is not defined.")
        return ""
    try:
        soup = BeautifulSoup(html.read(), "html.parser")
        title = soup.find('h1').getText()
    except AttributeError:
        print("Tag was not found")
        return ""
    return title


def prepare_post_url_data(request_data):
    errors = {}
    data = {}
    short_uuid_url = short_url_generator()
    if request_data.get("short_url"):
        if 4 > len(request_data["short_url"]) or len(request_data["short_url"]) > 8:
            errors['short_url'] = "Short URL will be at least" \
                                  " 4 chars and max 8 chars"
    if not request_data.get("short_url") or request_data.get("short_url") == "":
        request_data["short_url"] = f'{DEFAULT_DOMAIN}/{short_url_generator()}'
    title = get_title(request_data["url"])
    data["uuid"] = str(uuid.uuid4())
    data["url"] = request_data["url"]
    data["title"] = title
    data["domain"] = str(DEFAULT_DOMAIN)
    data["short_url"] = request_data["short_url"]
    data["slug"] = short_uuid_url
    data["clicks"] = 0
    data["create_dttm"] = f"{datetime.today()}"
    return errors, data


class MyView(HTTPMethodView):

    async def get(self, request):
        query_result = await db_conn.get_all("url_app_url")
        columns = ("id", "uuid", "url", "title", "domain", "short_url", "rel", "clicks", "create_dttm")
        exclude_fields = ("id", "domain", "rel")
        result = response_converter(query_result, columns, exclude_fields)
        return response.json(result)

    async def post(self, request):
        form_data, _ = CreateNewShortUrlForm().load(request.json)
        errors, data = prepare_post_url_data(form_data)
        if errors:
            return response.json(errors, HTTPStatus.BAD_REQUEST)
        try:
            await db_conn.insert("url_app_url", tuple(data.values()),
                                 ("uuid", "url", "title", "domain", "short_url", "slug", "clicks", "create_dttm"))
        except psycopg2.ProgrammingError as e:
            print(e)
            return response.json({"error": e}, HTTPStatus.BAD_REQUEST)

        query_result = await db_conn.get("url_app_url", ["*"], conditions_list=[("uuid", "=", data["uuid"], None)])
        columns = ("id", "uuid", "url", "title", "domain", "short_url", "rel", "clicks", "create_dttm")
        exclude_fields = ("id", "domain", "rel")
        result = response_converter(query_result, columns, exclude_fields)
        return response.json(result[0], HTTPStatus.CREATED)


class NewView(HTTPMethodView):

    async def get(self, request):
        query_result = await db_conn.full_join(
            "url_app_url", "url_app_profile", ("url_app_url.id", "=", "url_app_profile.id"))
        columns = ("id", "uuid", "url", "title", "domain", "short_url", "rel", "clicks", "create_dttm",
                   "id", "name", "email_confirmed", "user_id")
        exclude_fields = ("id", "domain", "rel")
        result = response_converter(query_result, columns, exclude_fields)
        return response.json(result)


app.add_route(MyView.as_view(), '/demo')
app.add_route(NewView.as_view(), '/new')
if __name__ == "__main__":
    app.run(host="localhost", port="8000")
