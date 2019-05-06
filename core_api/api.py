from sanic import Blueprint
from .app import app
from .resources import UrlsView, NewView

api_v1 = Blueprint("v1", url_prefix="/api/v1", strict_slashes=False)

api_v1.add_route(UrlsView.as_view(), '/urls', strict_slashes=False)
api_v1.add_route(NewView.as_view(), '/new', strict_slashes=False)

app.blueprint(api_v1)
