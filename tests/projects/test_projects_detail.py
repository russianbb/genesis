import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_projects_detail_not_logged(client, project):
    uri = reverse("projects:detail", args=[project.id])
    response = client.get(uri)

    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/projetos/1"


# def test_projects_detail_logged(client_logged, project):
#     uri = reverse("projects:detail", args=[project.id])
#     response = client_logged.get(uri)

#     assert response.status_code == 200
