from lemkpg import AsyncLemkPgApi

db_conn = AsyncLemkPgApi(db_name="urls_database", db_password="postgres", db_user="postgres", db_host="localhost")

DEFAULT_DOMAIN = "http://localhost:8000"
DB_NAME = "urls_database"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"

URLS_TABLE = "app_url"
USER_TABLE = "app_user"
USER_URLS_TABLE = "user_urls"
URLS_COLUMNS = ("id", "uuid", "url", "title", "domain", "short_url", "slug", "clicks", "create_dttm")
USER_COLUMNS = ("id", "uuid", "username", "password", "token")
