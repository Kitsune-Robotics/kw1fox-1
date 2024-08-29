import logging
import asyncio

from .base_task import Task


class UpdateWeather(Task):
    interval = 10  # Interval in seconds

    async def init(self):
        self.runs = 3

    async def run(self):
        # Your logic to update weather estimates goes here.
        await asyncio.sleep(1)  # Simulate task delay
        logging.debug("No weather to report")

        self.runs = self.runs - 1

        logging.debug(f"Runs is {self.runs}/0")
        if self.runs < 0:
            raise IndexError("There was an error!")
