import asyncio
import importlib
import os
import inspect
import logging

from .base_task import Task

# Keep track of running tasks
running_tasks = {}


async def run_task(task_instance):
    """Run a given task instance at its specified interval."""
    try:
        logging.info(f"Initializing {task_instance.name}")

        # Run the init method if it exists
        if hasattr(task_instance, "init"):
            await task_instance.init()

        # Loop the run function
        while True:
            logging.debug(f"Running {task_instance.name}")
            await task_instance.run()
            await asyncio.sleep(task_instance.interval)
    except Exception as e:
        logging.error(f"Error in task {task_instance.name}: {e}")


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
    logging.debug(f"Loaded tasks: {[task.__class__.__name__ for task in tasks]}")
    return tasks


async def start_scheduled_tasks():
    """Start all dynamically loaded scheduled tasks."""
    logging.debug("Loading tasks...")
    tasks = load_tasks()

    for task in tasks:
        # Create and start tasks while tracking them
        running_task = asyncio.create_task(run_task(task))
        running_tasks[task.name] = running_task
    await asyncio.gather(*running_tasks.values())
