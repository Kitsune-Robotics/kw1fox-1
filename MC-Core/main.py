import sys
import asyncio
import logging
import psycopg2

from aiohttp import web

from psycopg2.extras import RealDictCursor

from db import init_db

from healthcheck import health_check

from endpoints.example_endpoint import example_endpoint
from endpoints.task_endpoints import status, task_info

from tasks.task_scheduler import start_scheduled_tasks


async def create_app():
    app = web.Application()

    # Database initialization
    await init_db(app)

    # Setup routes
    app.router.add_get("/health", health_check)
    app.router.add_get("/status", status)
    app.router.add_get("/task_info/{task_name}", task_info)

    # Start scheduled tasks dynamically
    asyncio.create_task(start_scheduled_tasks())

    return app


async def main():
    # Create and run the web app
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8501)
    await site.start()

    # Run indefinitely, keeping the event loop alive
    while True:
        await asyncio.sleep(3600)


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

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Shutting down.")
