import factory
from faker import Factory as FakerFactory
from pytest_factoryboy import register
import pytest

from app.tasks.models import Task
from app.tasks.schema import TaskSchema


faker = FakerFactory.create()


@register(_name='tasks')
class TaskFactory(factory.Factory):
    class Meta:
        model = Task

    id = factory.LazyFunction(lambda: faker.random_int())
    name = factory.LazyFunction(lambda: faker.name())
    pomodoro_count = factory.LazyFunction(lambda: faker.random_int())
    category_id = factory.LazyFunction(lambda: faker.random_int())
    user_id = factory.LazyFunction(lambda: faker.random_int())  # Maybe str


def task(tasks):
    return tasks


def get_task_id():
    return 123


def get_task_name():
    return 'test_name'


def get_task_pomodoro_count():
    return 10


def get_task_category_id():
    return 456


def get_task_user_id():
    return 567
