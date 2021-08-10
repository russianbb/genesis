import pytest


@pytest.fixture()
def hello():
    return "hello"


@pytest.fixture()
def client_logged(db, client, django_user_model):
    user = django_user_model.objects.create_user(username="foo", password="bar")
    client.force_login(user=user)
    return client
