import contextvars
from sanic import Blueprint
from sanic import Sanic
from lemkpg.constants import GET_ALL_COLUMNS
from sanic.exceptions import Unauthorized

from core_api.resources import UrlsView, UrlView, RegisterView, AuthView, RedirectView
from core_api.config import USER_TABLE, USER_COLUMNS, db_conn, test_db_conn
from core_api.utils import response_converter


app = Sanic("app")


@app.middleware('request')
async def check_run_or_test_and_return_db_conn(request):
    ctx = contextvars.copy_context()
    context_values = list(ctx.values())
    if "default_context" in context_values:
        request["db_conn"] = db_conn
    if "test_context" in context_values:
        request["db_conn"] = test_db_conn
    else:
        request["db_conn"] = db_conn


@app.middleware('request')
async def check_authorization_and_add_user_to_request(request):
    registration_and_auth_paths = ["/api/v1/auth", "/api/v1/register"]
    api_path = "/api/v1/"
    if not request.token and request.path not in registration_and_auth_paths and api_path in request.path:
        raise Unauthorized("Authorization should be defined in request headers")
    else:
        result = await request["db_conn"].get(USER_TABLE, GET_ALL_COLUMNS,
                                              conditions_list=[("token", "=", request.token, None)])
        if not result and request.path not in registration_and_auth_paths and api_path in request.path:
            raise Unauthorized("Authorization with Token should be defined in request headers")
        if result and request.path not in registration_and_auth_paths and api_path in request.path:
            user = response_converter(result, USER_COLUMNS, ("password",))[0]
            request["user"] = user


def create_api():
    api_v1 = Blueprint("v1", url_prefix="/api/v1", strict_slashes=False)

    api_v1.add_route(UrlsView.as_view(), '/urls', strict_slashes=False)
    api_v1.add_route(UrlView.as_view(), '/urls/<url_uuid:uuid>', strict_slashes=False)
    api_v1.add_route(RegisterView.as_view(), '/register', strict_slashes=False)
    api_v1.add_route(AuthView.as_view(), '/auth', strict_slashes=False)
    app.add_route(RedirectView.as_view(), '/<slug>', strict_slashes=False)

    app.blueprint(api_v1)
