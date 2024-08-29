from aiohttp import web
import logging
from tasks.task_scheduler import running_tasks


async def status(request):
    """Status endpoint to return the health of all tasks."""
    task_statuses = {}

    for task_name, task in running_tasks.items():
        if task.done():
            if task.exception():
                task_statuses[task_name] = "UNHEALTHY"
            else:
                task_statuses[task_name] = "STOPPED"
        else:
            task_statuses[task_name] = "HEALTHY"

    return web.json_response(
        {
            "status": (
                "HEALTHY"
                if all(status == "HEALTHY" for status in task_statuses.values())
                else "UNHEALTHY"
            ),
            "tasks": task_statuses,
        }
    )
