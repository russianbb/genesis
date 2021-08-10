import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_projects_list_not_logged(client):
    uri = reverse("projects:list")
    response = client.get(uri)

    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/projetos/"


def test_projects_list_logged(client_logged):
    uri = reverse("projects:list")
    response = client_logged.get(uri)

    assert response.status_code == 200
