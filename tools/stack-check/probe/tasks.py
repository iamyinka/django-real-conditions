from celery import shared_task
from django.tasks import task


@shared_task
def add(x, y):
    return x + y


@task
def multiply(x, y):
    return x * y
