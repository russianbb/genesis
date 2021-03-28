import pytest
from django.contrib.auth.models import User


@pytest.fixture()
def hello():
    return "hello"


@pytest.fixture()
def super_user():
    return User.objects.create_user(
        username="fakeadmin", first_name="Fake", last_name="Admin", is_superuser=True
    )


@pytest.fixture()
def user():
    return User.objects.create_user(
        username="fakeuser", first_name="Fake", last_name="User", is_superuser=False
    )
