from core_api.config import db_conn
import asyncio


async def check_user_tables_existing():
    query = "SELECT 'public.app_user', 'public.user_urls'::regclass"
    result = await db_conn.raw_query(query)
    if 'public.app_user' not in result[0] and 'user_urls' not in result[0]:
        await create_user_tables()
    elif 'public.app_user' in result[0] and 'user_urls' not in result[0]:
        print(f"User table: 'user_urls' does not exist in DB")
    elif 'user_urls' in result[0] and 'public.app_user' not in result[0]:
        print(f"User table: 'public.app_user' does not exist in DB")
    else:
        print(f"User tables: {result[0]} exists in DB")


# Create user table:
async def create_user_tables():
    user_query = """
    CREATE TABLE public.app_user (
    id integer DEFAULT NULL,
    uuid uuid NOT NULL,
    username character varying(100) NOT NULL,
     password character varying(100) NOT NULL,
     token character varying(256) NOT NULL,
     CONSTRAINT app_user_pkey PRIMARY KEY (id))
    """
    seq_query = "CREATE sequence app_user_id_seq owned by app_user.id"
    id_query = "ALTER TABLE app_user alter column id set default nextval('app_user_id_seq')"
    await db_conn.raw_query(user_query)
    await db_conn.raw_query(seq_query)
    await db_conn.raw_query(id_query)

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
  CONSTRAINT user_urls_url_id_5de65233_fk_url_app_url_id FOREIGN KEY (url_id)
      REFERENCES public.url_app_url (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT user_urls_user_id_url_id_2655d850_uniq UNIQUE (user_id, url_id)
)
WITH (
  OIDS=FALSE
)
     """
    seq_query = "CREATE sequence user_urls_id_seq owned by user_urls.id"
    id_query = "ALTER TABLE user_urls alter column id set default nextval('user_urls_id_seq')"
    await db_conn.raw_query(user_urls_query)
    await db_conn.raw_query(seq_query)
    await db_conn.raw_query(id_query)

    print("User Table`s created!")


def setup():
    asyncio.run(check_user_tables_existing())


if __name__ == "__main__":
    setup()
