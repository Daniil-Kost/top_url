from lemkpg import AsyncLemkPgApi
from sanic import Sanic
from sanic import Blueprint


app = Sanic("app")
db_conn = AsyncLemkPgApi(db_name="urls_database", db_password="postgres", db_user="postgres", db_host="localhost")

if __name__ == "__main__":
    app.run(host="localhost", port="8000")
