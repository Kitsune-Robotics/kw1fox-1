import asyncio
import logging

from .base_task import Task


class CheckLastTransmission(Task):
    interval = 10  # Interval in seconds

    async def init(self):
        logging.info("Initializing and checking DB")

    async def run(self):
        logging.info(f"Running task: {self.name}")
        # Your logic to check the last transmission time goes here.
        await asyncio.sleep(1)  # Simulate task delay
        logging.info("Last transmission check completed.")
