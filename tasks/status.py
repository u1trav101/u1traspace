from celery import current_app


def get_scheduled_tasks():
    inspect = current_app.control.inspect()
    tasks = inspect.scheduled()
    key = next(iter(tasks))
    tasks = tasks[key]

    return tasks if len(tasks) > 0 else None

def get_running_tasks():
    inspect = current_app.control.inspect()
    tasks =  inspect.active()
    key = next(iter(tasks))
    tasks = tasks[key]

    return tasks if len(tasks) > 0 else None
