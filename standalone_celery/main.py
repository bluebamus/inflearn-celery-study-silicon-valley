from celery import Celery

app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["worker.tasks"],
)

# app = Celery('worker',
#              include=['worker.tasks'])

# app.config_from_object('celeryconfig')

# routing 첫번째 방법
app.conf.update(
    worker_concurrency=4,  # worker 개수를 4개로 설정
    task_routes={
        "worker.tasks.add": {"queue": "queue2"},
        "worker.tasks.mul": {"queue": "queue2"},
        "worker.tasks.xsum": {"queue": "queue2"},
    },
)

# routing 두번째 방법
# app.conf.task_routes = {
#     "worker.tasks.add": {"queue": "queue2"},
#     "worker.tasks.mul": {"queue": "queue2"},
#     "worker.tasks.xsum": {"queue": "queue2"},
# }

if __name__ == "__main__":
    app.start()
