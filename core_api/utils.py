import uuid
import secrets
import shortuuid
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import urlopen
from urllib.error import HTTPError

from .config import DEFAULT_DOMAIN, USER_TABLE, USER_URLS_TABLE, URLS_TABLE, db_conn


# convert response to dict
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
    data = {}
    short_uuid_url = short_url_generator()
    if not request_data.get("short_url") or request_data.get("short_url") == "":
        request_data["short_url"] = f'{DEFAULT_DOMAIN}/{short_uuid_url}'
    title = get_title(request_data["url"])
    data["uuid"] = str(uuid.uuid4())
    data["url"] = request_data["url"]
    data["title"] = title
    data["domain"] = str(DEFAULT_DOMAIN)
    data["short_url"] = request_data["short_url"]
    data["slug"] = short_uuid_url
    data["clicks"] = 0
    data["create_dttm"] = f"{datetime.today()}"
    return data


def prepare_user_registration_data(request_data):
    data = {}
    data["uuid"] = str(uuid.uuid4())
    data["username"] = request_data["username"]
    data["password"] = request_data["password"]
    data["token"] = secrets.token_hex(40)
    return data


async def check_username_existing(db_connection, username):
    result = await db_connection.get(USER_TABLE, ["id"], conditions_list=[("username", "=", username, None)])
    return True if result else False


async def get_url_by_uuid(db_connection, url_uuid, request_user_id):
    query = f"""SELECT * FROM {URLS_TABLE} FULL JOIN {USER_URLS_TABLE} 
           ON {USER_URLS_TABLE}.user_id = {request_user_id}
           AND {URLS_TABLE}.uuid = '{url_uuid}' WHERE {URLS_TABLE}.id IN ({USER_URLS_TABLE}.url_id)"""
    query_result = await db_connection.raw_query(query)
    return query_result


async def get_user_urls(db_connection, request_user_id):
    query = f"""SELECT * FROM {URLS_TABLE} FULL JOIN {USER_URLS_TABLE} 
               ON {USER_URLS_TABLE}.user_id = {request_user_id}
               WHERE {URLS_TABLE}.id IN ({USER_URLS_TABLE}.url_id)"""
    query_result = await db_connection.raw_query(query)
    return query_result
