from lemkpg import AsyncLemkPgApi

db_conn = AsyncLemkPgApi(db_name="urls_database", db_password="postgres", db_user="postgres", db_host="localhost")

DEFAULT_DOMAIN = "http://localhost:8000"
DB_NAME = "urls_database"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"

URLS_TABLE = "app_url"
PROFILE_TABLE = "app_user"
URLS_COLUMNS = ("id", "uuid", "url", "title", "domain", "short_url", "slug", "clicks", "create_dttm")
PROFILE_COLUMNS = ("id", "uuid", "username", "password", "token")
