DEFAULT_DOMAIN = "http://localhost:8000"
DB_NAME = "urls_database"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"

URLS_TABLE = "url_app_url"
PROFILE_TABLE = "url_app_profile"
URLS_COLUMNS = ("id", "uuid", "url", "title", "domain", "short_url", "slug", "clicks", "create_dttm")
PROFILE_COLUMNS = ("id", "name", "email_confirmed", "user_id")
