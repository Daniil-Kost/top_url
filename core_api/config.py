import os
from lemkpg import AsyncLemkPgApi


DEFAULT_DOMAIN = os.environ.get("DEFAULT_DOMAIN", "http://localhost:8000")
DB_NAME = os.environ.get("DB_NAME", "urls_database")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_HOST = os.environ.get("DB_HOST", "localhost")

URLS_TABLE = "app_url"
USER_TABLE = "app_user"
USER_URLS_TABLE = "user_urls"
URLS_COLUMNS = ("id", "uuid", "url", "title", "domain", "short_url", "slug", "clicks", "create_dttm")
USER_COLUMNS = ("id", "uuid", "username", "password", "token")
USER_URLS_COLUMNS = ("id", "user_id", "url_id")

db_conn = AsyncLemkPgApi(db_name=DB_NAME, db_password=DB_PASSWORD, db_user=DB_USER, db_host=DB_HOST)
test_db_conn = AsyncLemkPgApi(db_name="urls_test", db_password="postgres", db_user="postgres", db_host="localhost")
