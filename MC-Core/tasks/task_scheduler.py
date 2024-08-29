import asyncio
import logging
import importlib
import os
import inspect
from .base_task import Task


async def run_task(task_instance):
    """Run a given task instance at its specified interval."""

    # Run the init
    await task_instance.init()

    # Loop the run function
    while True:
        await task_instance.run()
        await asyncio.sleep(task_instance.interval)


def load_tasks():
    """Dynamically load task classes from the tasks directory."""
    tasks = []
    task_directory = os.path.dirname(__file__)
    for filename in os.listdir(task_directory):
        if filename.endswith(".py") and filename not in (
            "__init__.py",
            "base_task.py",
            "task_scheduler.py",
        ):
            module_name = f"tasks.{filename[:-3]}"
            module = importlib.import_module(module_name)
            for attr in dir(module):
                obj = getattr(module, attr)
                if inspect.isclass(obj) and issubclass(obj, Task) and obj is not Task:
                    tasks.append(obj())

            logging.info(f"Loaded {filename} as a task. Module was {module_name}")
    return tasks


async def start_scheduled_tasks():
    """Start all dynamically loaded scheduled tasks."""
    tasks = load_tasks()
    for task in tasks:
        logging.debug(f"Starting {task}")
    running_tasks = [run_task(task) for task in tasks]

    await asyncio.gather(*running_tasks)
    logging.debug("All tasks Started!")
