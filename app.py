from lemkpg import AsyncLemkPgApi
from sanic import Sanic
from sanic import Blueprint

from core_api.resources import UrlsView, UrlView, RegisterView

app = Sanic("app")

api_v1 = Blueprint("v1", url_prefix="/api/v1", strict_slashes=False)

api_v1.add_route(UrlsView.as_view(), '/urls', strict_slashes=False)
api_v1.add_route(UrlView.as_view(), '/urls/<url_uuid:uuid>', strict_slashes=False)
api_v1.add_route(RegisterView.as_view(), '/register', strict_slashes=False)

app.blueprint(api_v1)


if __name__ == "__main__":
    app.run(host="localhost", port="8000")
