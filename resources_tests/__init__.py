import unittest
import pickle
from core_api.config import db_conn
from core_api import config

#
# default_db_name = {"DB_CONN_DSN": db_conn.dsn}
# data = pickle.dumps(default_db_name)


# def set_test_env_variables():
#     db_conn.dsn = f"dbname=test_urls_db user=postgres password=postgres host=localhost"
#
#
# def del_test_env_variables_and_set_default():
#     db_name = pickle.loads(data)["DB_CONN_DSN"]
#     db_conn.dsn = db_name


