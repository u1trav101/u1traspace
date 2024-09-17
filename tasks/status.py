from celery import current_app


def get_scheduled_tasks() -> list | None:
    inspect = current_app.control.inspect()
    tasks: list = inspect.scheduled()
    key: int = next(iter(tasks))
    tasks = tasks[key]

    return tasks if len(tasks) > 0 else None


def get_running_tasks() -> list | None:
    inspect = current_app.control.inspect()
    tasks: list = inspect.active()
    key: int = next(iter(tasks))
    tasks = tasks[key]

    return tasks if len(tasks) > 0 else None
