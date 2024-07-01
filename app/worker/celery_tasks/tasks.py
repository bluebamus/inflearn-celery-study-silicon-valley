import logging
import time
import traceback
from celery import Task, group
from worker.celery import app
from worker.tasks import add


# @app.task(queue="celery")
# def my_super_task():
#     try:
#         raise IOError("File X does not exists")
#     except IOError as e:
#         logging.error(e)


# Define custom task class
class CustomTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # exc: The exception that caused the task to fail.
        # task_id: The ID of the failed task.
        # args: The arguments passed to the task.
        # kwargs: The keyword arguments passed to the task.
        # einfo: An object containing information about the exception.

        # This method is called when a task fails
        print(f"Task failed: {exc}")

        # Optionally, you can perform actions like logging or sending notifications here
        # For example, you might want to retry the task under certain conditions
        if isinstance(exc, Exception):
            logging.error(f"Error happens on {task_id}... fix this!!!")


# Register custom task class with Celery
app.task(base=CustomTask)


@app.task(
    queue="celery",
    base=CustomTask,
    autoretry_for=(IOError,),
    max_retries=3,
    default_retry_delay=10,
)
def my_super_task():
    # try:
    raise IOError("File X does not exists")
    # except IOError as e:
    #     logging.error(e)
