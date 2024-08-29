import asyncio
import psycopg2
import logging

from os import getenv
from psycopg2.extras import RealDictCursor


async def init_db(app):
    # Get environment variables
    _db = getenv("POSTGRES_DB", "postgres")
    _user = getenv("POSTGRES_USER", "postgres")
    _pass = getenv("POSTGRES_PASSWORD", "postgres")
    _host = getenv("POSTGRES_HOST", "db")

    logging.info(f"Connecting to {_host} with login {_user}@{_db}")

    # Retry parameters
    max_retries = 3
    retry_delay = 5  # seconds

    # Attempt to connect to the database with retry logic
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname=_db,
                user=_user,
                password=_pass,
                host=_host,
                cursor_factory=RealDictCursor,
            )

            # Store the connection in the app
            app["db"] = conn

            async def close_db(app):
                conn.close()

            app.on_cleanup.append(close_db)

            logging.info("Connected to the database successfully.")
            return  # Exit if connection is successful

        except psycopg2.OperationalError as e:
            logging.warning(
                f"Database connection failed on attempt {attempt + 1}/{max_retries}: {e}"
            )
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)  # Wait before retrying
            else:
                logging.error(
                    "Failed to connect to the database after multiple attempts."
                )
                raise
