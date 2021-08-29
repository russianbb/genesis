import pytest


@pytest.fixture()
def hello():
    return "hello"


@pytest.fixture()
def client_logged(db, client, django_user_model):
    user = django_user_model.objects.create_user(username="foo", password="bar")
    client.force_login(user=user)
    return client


@pytest.fixture()
def user(django_user_model):
    return django_user_model.objects.create(
        username="financeiro", password="1234", email="financeiro@onixse.com"
    )
