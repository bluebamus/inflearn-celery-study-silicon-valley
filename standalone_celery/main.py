from celery import Celery

app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["worker.tasks"],
)

app.conf.task_default_queue = "celery"

# app = Celery('worker',
#              include=['worker.tasks'])

# app.config_from_object('celeryconfig')

# routing 첫번째 방법
# app.conf.update(
#     worker_concurrency=4,  # worker 개수를 4개로 설정
#     task_routes={
#         "worker.tasks.add": {"queue": "queue2"},
#         "worker.tasks.mul": {"queue": "queue2"},
#         "worker.tasks.xsum": {"queue": "queue2"},
#     },
# )

# routing 두번째 방법
# app.conf.task_routes = {
#     "worker.tasks.add": {"queue": "queue2"},
#     "worker.tasks.mul": {"queue": "queue2"},
#     "worker.tasks.xsum": {"queue": "queue2"},
# }


# task grouping
app.conf.update(
    worker_concurrency=4,  # worker 개수를 4개로 설정
    task_routes={
        "worker.tasks.add": {"queue": "celery"},
        "worker.tasks.mul": {"queue": "celery"},
        "worker.tasks.xsum": {"queue": "celery"},
    },
)

app.conf.task_default_rate_limit = "5/m"

app.conf.broker_transport_options = {
    "priority_steps": list(range(10)),  # default is 4
    # "sep": ":",
    "queue_order_strategy": "priority",
}

"""
['celery', 'celery:1', 'celery:2', 'celery:3', 'celery:4', 'celery:5', 'celery:6', 'celery:7', 'celery:8', 'celery:9']
"""
app.conf.broker_connection_retry_on_startup = True

if __name__ == "__main__":
    app.start()
