import sys
import asyncio
import logging
import psycopg2

from aiohttp import web

from psycopg2.extras import RealDictCursor

from db import init_db
from healthcheck import health_check
from endpoints import example_endpoint
from tasks.task_scheduler import start_scheduled_tasks


async def create_app():
    app = web.Application()

    # Database initialization
    await init_db(app)

    # Setup routes
    app.router.add_get("/health", health_check)
    # app.router.add_get("/example", example_endpoint)

    # Start scheduled tasks dynamically
    asyncio.create_task(start_scheduled_tasks())

    return app


if __name__ == "__main__":
    # Setup logging
    if True:  # TODO os.getenv here
        logging.basicConfig(
            stream=sys.stderr,
            level=logging.DEBUG,
            format="%(levelname)s:%(name)s: %(message)s",
        )
        logging.debug("Running in debug mode.")
    else:
        logging.basicConfig(
            stream=sys.stderr,
            level=logging.INFO,
            format="%(levelname)s:%(name)s: %(message)s",
        )
        logging.info("Running in prod mode.")

    # Create app
    app = asyncio.run(create_app())

    # Run app
    web.run_app(app, host="0.0.0.0", port=8501)
