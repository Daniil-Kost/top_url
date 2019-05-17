from sanic import Blueprint
from sanic import Sanic

from core_api.resources import UrlsView, UrlView, RegisterView, AuthView, RedirectView, DemoView


app = Sanic("app")


def create_api():
    api_v1 = Blueprint("v1", url_prefix="/api/v1", strict_slashes=False)

    api_v1.add_route(UrlsView.as_view(), '/urls', strict_slashes=False)
    api_v1.add_route(UrlView.as_view(), '/urls/<url_uuid:uuid>', strict_slashes=False)
    api_v1.add_route(RegisterView.as_view(), '/register', strict_slashes=False)
    api_v1.add_route(AuthView.as_view(), '/auth', strict_slashes=False)
    app.add_route(RedirectView.as_view(), '/<slug>', strict_slashes=False)

    app.add_route(DemoView.as_view(), "/", strict_slashes=False)

    app.blueprint(api_v1)
