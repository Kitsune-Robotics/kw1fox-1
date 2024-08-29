import logging
import asyncio

from .base_task import Task


class UpdateWeather(Task):
    interval = 300  # Interval in seconds

    async def run(self):
        # Your logic to update weather estimates goes here.
        await asyncio.sleep(1)  # Simulate task delay
        logging.debug("No weather to report")
