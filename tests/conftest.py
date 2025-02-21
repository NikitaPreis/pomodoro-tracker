import asyncio

import pytest

pytest_plugins = [
    'tests.fixtures.auth.auth_service',
    'tests.fixtures.auth.clients',
    'tests.fixtures.tasks.task_cache',
    'tests.fixtures.tasks.task_repository',
    'tests.fixtures.tasks.task_model',
    'tests.fixtures.tasks.task_schemas',
    'tests.fixtures.tasks.task_service',
    'tests.fixtures.users.user_repository',
    'tests.fixtures.users.user_model',
    'tests.fixtures.users.user_service',
    'tests.fixtures.infrastructure',
]


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
