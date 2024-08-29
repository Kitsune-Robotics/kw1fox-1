import asyncio
import psycopg2
import logging

from os import getenv

from psycopg2.extras import RealDictCursor


async def init_db(app):
    # Get envs
    _db = getenv("POSTGRES_DB", "postgres")
    _user = getenv("POSTGRES_USER", "postgres")
    _pass = getenv("POSTGRES_PASSWORD", "postgres")
    _host = getenv("POSTGRES_HOST", "db")

    logging.info(f"Connecting to {_host} with login {_user}@{_db}")

    conn = psycopg2.connect(
        dbname=_db,
        user=_user,
        password=_pass,
        host=_host,
        cursor_factory=RealDictCursor,
    )

    app["db"] = conn

    async def close_db(app):
        conn.close()

    app.on_cleanup.append(close_db)
