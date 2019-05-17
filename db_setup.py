import asyncio
import argparse
import sys


from core_api.config import db_conn

parser = argparse.ArgumentParser(description="DB Setup args")

parser.add_argument("-d", "--delete", action="store_true")
parser.add_argument("-c", "--clear", action="store_true")
args = parser.parse_args()

if args.delete:
    async def delete_tables():
        await db_conn.delete_table("public.user_urls")
        await db_conn.delete_table("public.app_url")
        await db_conn.delete_table("public.app_user")
        print("All tables successfully deleted!")
        sys.exit()
    asyncio.run(delete_tables())

if args.clear:
    async def clear_tables():
        exists_user_urls = await db_conn.raw_query("SELECT to_regclass('public.user_urls')")
        exists_app_url = await db_conn.raw_query("SELECT to_regclass('public.app_url')")
        exists_app_user = await db_conn.raw_query("SELECT to_regclass('public.app_user')")
        exists_list = [exists_user_urls[0][0], exists_app_url[0][0], exists_app_user[0][0]]
        if "user_urls" in exists_list and "app_url" in exists_list and "app_user" in exists_list:
            await db_conn.clear_table("user_urls, app_url, app_user")
            print("All tables successfully cleared!")
        else:
            print("Cannot clear all tables - some tables are not defined")
        sys.exit()
    asyncio.run(clear_tables())


# check existing users tables (public.app_user')
async def _check_user_table_existing():
    query = "SELECT to_regclass('public.app_user')"
    result = await db_conn.raw_query(query)
    if 'app_user' not in result[0]:
        await create_user_table()
    else:
        print(f"User table: 'app_user' exists in DB")


# check existing url table (public.app_url')
async def _check_url_table_existing():
    query = "SELECT to_regclass('public.app_url')"
    result = await db_conn.raw_query(query)
    if 'app_url' not in result[0]:
        await create_url_table()
    else:
        print(f"Url table: 'app_url' exists in DB")


# check existing url table (public.user_urls')
async def _check_user_urls_table_existing():
    query = "SELECT to_regclass('public.user_urls')"
    result = await db_conn.raw_query(query)
    if 'user_urls' not in result[0]:
        await create_user_urls_table()
    else:
        print(f"User Urls table: 'user_urls' exists in DB")


async def check_existing_tables():
    await _check_user_table_existing()
    await _check_url_table_existing()
    await _check_user_urls_table_existing()


# Create user table:
async def create_user_table():
    user_query = """
    CREATE TABLE public.app_user (
    id integer DEFAULT NULL,
    uuid uuid NOT NULL,
    username character varying(100) NOT NULL,
     password character varying(100) NOT NULL,
     token character varying(256) NOT NULL,
     CONSTRAINT app_user_pkey PRIMARY KEY (id))
    """

    user_seq_query = "CREATE sequence app_user_id_seq owned by app_user.id"

    user_id_query = "ALTER TABLE app_user alter column id set default nextval('app_user_id_seq')"

    await db_conn.raw_query(user_query)
    await db_conn.raw_query(user_seq_query)
    await db_conn.raw_query(user_id_query)

    print("app_user table successfully created!")


# Create user urls table:
async def create_user_urls_table():
    user_urls_query = """
    CREATE TABLE user_urls
    (
    id integer DEFAULT NULL,
    user_id integer NOT NULL,
    url_id integer NOT NULL,
    CONSTRAINT user_urls_pkey PRIMARY KEY (id),
    CONSTRAINT user_urls_profile_id_8e86bcdb_fk_user_id FOREIGN KEY (user_id)
      REFERENCES public.app_user (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
      CONSTRAINT user_urls_url_id_5de65233_fk_app_url_id FOREIGN KEY (url_id)
      REFERENCES app_url (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
      CONSTRAINT user_urls_user_id_url_id_2655d850_uniq UNIQUE (user_id, url_id)
      )
      WITH (
      OIDS=FALSE
      )
     """

    user_urls_seq_query = "CREATE sequence user_urls_id_seq owned by user_urls.id"

    user_urls_id_query = "ALTER TABLE user_urls alter column id set default nextval('user_urls_id_seq')"

    await db_conn.raw_query(user_urls_query)
    await db_conn.raw_query(user_urls_seq_query)
    await db_conn.raw_query(user_urls_id_query)

    print("user_urls table successfully created!")


# Create url table:
async def create_url_table():
    query = """
    CREATE TABLE public.app_url
    (
    id integer DEFAULT NULL,
    uuid uuid NOT NULL,
    url character varying(256) NOT NULL,
    title character varying(256) NOT NULL,
    domain character varying(96) NOT NULL,
    short_url character varying(256) NOT NULL,
    slug character varying(50) NOT NULL,
    clicks integer NOT NULL,
    create_dttm timestamp with time zone NOT NULL,
    CONSTRAINT app_url_pkey PRIMARY KEY (id),
    CONSTRAINT app_url_short_url_key UNIQUE (short_url),
    CONSTRAINT app_url_uuid_key UNIQUE (uuid)
    )
    WITH (
    OIDS=FALSE
    )
    """

    seq_query = "CREATE sequence app_url_id_seq owned by app_url.id"

    id_query = "ALTER TABLE app_url alter column id set default nextval('app_url_id_seq')"

    index_short_url_query = """
    CREATE INDEX app_url_short_url_ff5b03fe_like ON public.app_url
    USING btree (short_url COLLATE pg_catalog."default" varchar_pattern_ops)
    """

    index_slug_query = """
    CREATE INDEX app_url_url_slug_51d6effc_like ON public.app_url
    USING btree (slug COLLATE pg_catalog."default" varchar_pattern_ops);
    """

    await db_conn.raw_query(query)
    await db_conn.raw_query(seq_query)
    await db_conn.raw_query(id_query)
    await db_conn.raw_query(index_short_url_query)
    await db_conn.raw_query(index_slug_query)

    print("app_url table successfully created!")


def setup():
    asyncio.run(check_existing_tables())


if __name__ == "__main__":
    setup()
