import logging

from datetime import datetime

from aiohttp import web

from tasks.task_scheduler import running_tasks, task_errors


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


async def task_info(request):
    """Return detailed information about a specific task."""
    task_name = request.match_info.get("task_name")

    if task_name not in running_tasks:
        return web.json_response(
            {"server_error": f"Task {task_name} not found"}, status=404
        )

    task = running_tasks[task_name]
    task_error = task_errors.get(task_name)

    try:
        if task.get_coro().cr_frame is not None:
            # Collect public attributes of the task instance
            public_attributes = {
                k: v
                for k, v in vars(
                    task.get_coro().cr_frame.f_locals["task_instance"]
                ).items()
                if not k.startswith("_")
            }
        else:
            public_attributes = {"_none": "No Local Values when STOPPED"}

        return web.json_response(
            {
                "task_name": task_name,
                "status": "RUNNING" if not task.done() else "STOPPED",
                "error": task_error,
                "public_attributes": public_attributes,
            }
        )
    except Exception as e:
        logging.error(f"Issue getting information for task {task_name}, error was {e}")
        return web.json_response(
            {
                "server_error": str(e),
                "task_name": task_name,
                "status": "RUNNING" if not task.done() else "STOPPED",
            }
        )
