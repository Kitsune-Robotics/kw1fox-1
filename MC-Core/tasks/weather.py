import asyncio
from .base_task import Task


class UpdateWeather(Task):
    interval = 60  # Interval in seconds

    async def init(self):
        pass

    async def run(self):
        print(f"Running task: {self.name}")
        # Your logic to update weather estimates goes here.
        await asyncio.sleep(1)  # Simulate task delay
        print("Weather update completed.")
