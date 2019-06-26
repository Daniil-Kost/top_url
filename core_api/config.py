import os
from jinja2 import Environment, PackageLoader, select_autoescape
from lemkpg import AsyncLemkPgApi


# application config variables
APP_HOST = os.environ.get("APP_HOST", "127.0.0.1")
APP_PORT = os.environ.get("APP_PORT", "8000")
DEFAULT_DOMAIN = os.environ.get("DEFAULT_DOMAIN", "http://127.0.0.1:8000")

# database config variables
DB_NAME = os.environ.get("DB_NAME", "urls_database")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_HOST = os.environ.get("DB_HOST", "localhost")

# test-connection database config
TEST_CONNECTION_DB_NAME = os.environ.get("TEST_CONNECTION_DB_NAME", "postgres")
TEST_CONNECTION_DB_USER = os.environ.get("TEST_CONNECTION_DB_USER", "postgres")
TEST_CONNECTION_DB_PASSWORD = os.environ.get("TEST_CONNECTION_DB_PASSWORD", "postgres")
TEST_CONNECTION_DB_HOST = os.environ.get("TEST_CONNECTION_DB_HOST", "localhost")

# test database config
TEST_DB_NAME = os.environ.get("TEST_DB_NAME", "urls_test")
TEST_DB_USER = os.environ.get("TEST_DB_USER", "postgres")
TEST_DB_PASSWORD = os.environ.get("TEST_DB_PASSWORD", "postgres")
TEST_DB_HOST = os.environ.get("TEST_DB_HOST", "localhost")

# db_structure vars
URLS_TABLE = "app_url"
USER_TABLE = "app_user"
USER_URLS_TABLE = "user_urls"
URLS_COLUMNS = ("id", "uuid", "url", "title", "domain", "short_url", "slug", "clicks", "create_dttm")
USER_COLUMNS = ("id", "uuid", "username", "password", "token")
USER_URLS_COLUMNS = ("id", "user_id", "url_id")

# lemkpg database connection objects
db_conn = AsyncLemkPgApi(db_name=DB_NAME, db_password=DB_PASSWORD, db_user=DB_USER, db_host=DB_HOST)
test_db_conn = AsyncLemkPgApi(db_name=TEST_DB_NAME, db_password=TEST_DB_PASSWORD,
                              db_user=TEST_DB_USER, db_host=TEST_DB_HOST)

# Jinja2 config vars
env = Environment(
    loader=PackageLoader('application', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('index.html')
