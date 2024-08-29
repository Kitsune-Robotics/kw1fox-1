import logging
from abc import ABC, abstractmethod


class Task(ABC):
    """Base Task class for defining scheduled tasks."""

    interval = 60  # Default interval in seconds

    def __init__(self):
        self.name = self.__class__.__name__

    async def init(self):
        """Runs only on startup"""
        logging.warn(f"Task {self.name} is using the default init!")

    @abstractmethod
    async def run(self):
        """Task-specific code to run at each interval."""
        logging.warn(f"Task {self.name} is using the default run!")
