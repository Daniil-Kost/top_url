from application import app, create_api
from core_api.config import APP_HOST, APP_PORT


def run_app():
    create_api()
    app.run(host=APP_HOST, port=APP_PORT, debug=False, access_log=True)


if __name__ == "__main__":
    run_app()
