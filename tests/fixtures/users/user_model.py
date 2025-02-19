import factory
import factory.fuzzy
from faker import Factory as FakerFactory
import pytest
from pytest_factoryboy import register

from app.users.user_profile.models import UserProfile

faker = FakerFactory.create()


@register(_name='user_profiles')
class UserProfileFactory(factory.Factory):

    class Meta:
        model = UserProfile

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    password = factory.LazyFunction(lambda: faker.password())
    email = factory.LazyFunction(lambda: faker.email())
    name = factory.LazyFunction(lambda: faker.name())
    yandex_access_token = factory.LazyFunction(lambda: faker.sha256())
    google_access_token = factory.LazyFunction(lambda: faker.sha256())


@pytest.fixture
def user_profile(user_profiles):
    return user_profiles

def get_fake_password():
    return 'fake_password'

def get_fake_user_id():
    return 123
