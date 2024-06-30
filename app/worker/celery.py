import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("worker")
# app.conf.update(
#     worker_concurrency=4,  # worker 개수를 4개로 설정
# )

app.conf.task_default_queue = "celery,3"

# task grouping
app.conf.update(
    worker_concurrency=4,  # worker 개수를 4개로 설정
    task_routes={
        "worker.tasks.dumb": {"queue": "celery,3"},
        "worker.tasks.add": {"queue": "celery,3"},
    },
)

app.conf.task_default_rate_limit = "5/m"

# # routing 첫번째 방법
# app.conf.update(
#     worker_concurrency=4,  # worker 개수를 4개로 설정
#     task_routes={
#         "worker.tasks.dumb": {"queue": "queue1"},
#         "worker.tasks.add": {"queue": "queue2"},
#     },
# )

# routing 두번째 방법
# app.conf.task_routes = {
#     "worker.tasks.dumb": {"queue": "queue1"},
#     "worker.tasks.add": {"queue": "queue2"},
# }

app.conf.broker_transport_options = {
    "priority_steps": list(range(10)),  # default is 4
    "sep": ":",
    "queue_order_strategy": "priority",
}

"""
['celery', 'celery:1', 'celery:2', 'celery:3', 'celery:4', 'celery:5', 'celery:6', 'celery:7', 'celery:8', 'celery:9']
"""

app.conf.broker_connection_retry_on_startup = True

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks(["worker", "worker.celery_tasks"])

# Periodic task & Cron Table
# app.conf.beat_schedule = {
#     "add-every-5-seconds": {
#         "task": timedelta(seconds=5),
#         "args": (10, 10),
#         # "kwargs": {"key": "value"},
#         # "options": {"queue": "celery"},
#     },
#     "add-every-minute": {
#         "task": "worker.tasks.add",
#         "scheduel": crontab(minute="*"),
#         "args": (20, 20),
#     },
# }


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
