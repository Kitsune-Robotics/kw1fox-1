from aiohttp import web
import logging
from tasks.task_scheduler import running_tasks


async def health_check(request):
    """Health check endpoint to ensure tasks are running."""
    unhealthy_tasks = []

    # Check the status of each task
    for task_name, task in running_tasks.items():
        if task.done():
            if task.exception():
                logging.error(
                    f"Task {task_name} has errored out with exception: {task.exception()}"
                )
            else:
                logging.warning(f"Task {task_name} has stopped unexpectedly.")
            unhealthy_tasks.append(task_name)

    if unhealthy_tasks:
        return web.json_response(
            {"status": "unhealthy", "unhealthy_tasks": unhealthy_tasks}, status=500
        )

    return web.json_response({"status": "healthy"})
