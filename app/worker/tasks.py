import time
from celery import shared_task
from celery.signals import task_prerun, task_postrun, task_failure

# @shared_task
# def add(x, y):
#     return x + y


# @shared_task
# def dumb():
#     return


# @shared_task(queue="celery")
# def p1():
#     time.sleep(5)


# @shared_task(queue="celery:1")
# def p2():
#     time.sleep(5)


# @shared_task(queue="celery:2")
# def p3():
#     time.sleep(5)


# task grouping
@shared_task(queue="celery")
def add(x, y):
    return x + y


@shared_task(queue="celery")
def dumb():
    return


@shared_task(queue="celery")
def xsum(numbers):
    return sum(numbers)


@shared_task(queue="celery")
def p1():
    time.sleep(5)


@shared_task(queue="celery")
def p2():
    time.sleep(5)


@shared_task(queue="celery")
def p3():
    time.sleep(5)


# keyword arg
@shared_task(queue="celery")
def print_result(x, y, msg=None):
    total = x + y
    if msg:
        return f"{msg}: {total}"
    return total


# Synchronous Task
def sync_task():
    result = sleep_task.apply_async()  # type: ignore
    print("Waiting ...")
    print(result.get())


# Asynchronous Task
def async_task():
    result = sleep_task.apply_async()  # type: ignore
    print("Not waiting ...")
    print(result.task_id)


# Define signal handlers
# @task_prerun.connect(sender=add)
# def task_prerun_handler(sender, task_id, task, args, kwargs, **kwargs_extra):
#     print(f"Task {task_id} is about to run: {task.name} with args {args}")


# @task_postrun.connect(sender=add)
# def task_postrun_handler(
#     sender, task_id, task, args, kwargs, retval, state, **kwargs_extra
# ):
#     print(f"Task {task_id} has completed: {task.name} with result {retval}")


# Define signal handlers
@task_prerun.connect
def task_prerun_handler(sender, task_id, task, args, kwargs, **kwargs_extra):
    print(f"Task {task_id} it about to run : {task.name} with args {args}")


@task_postrun.connect
def task_postrun_handler(
    sender, task_id, task, args, kwargs, retval, state, **kwargs_extra
):
    print(f"Task {task_id} has completed : {task.name} with result {retval}")


@task_failure.connect(sender=add)
def task_failure_handler(
    sender, task_id, exception, args, kwargs, traceback, einfo, **kwargs_extra
):
    print(f"Task {task_id} has failed: {sender.name} with exception {exception}")
    task_failure_clean_up.delay(task_id=task_id)  # type: ignore


@shared_task(queue="celery")
def task_failure_clean_up(task_id, *args, **kwargs):
    print(f"Task {task_id} clean up process has been started")


# simulating task signal
def simulating_task_signal():
    # Call the Celery task asynchronously
    result = add.delay(2, "error")  # type: ignore

    # Get the result of the task
    final_result = result.get()
    print("Final Result:", final_result)
