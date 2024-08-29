from abc import ABC, abstractmethod


class Task(ABC):
    """Base Task class for defining scheduled tasks."""

    interval = 60  # Default interval in seconds

    def __init__(self):
        self.name = self.__class__.__name__

    @abstractmethod
    async def init(self):
        """Runs only on startup"""
        pass

    @abstractmethod
    async def run(self):
        """Task-specific code to run at each interval."""
        pass
