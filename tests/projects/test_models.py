import pytest

pytestmark = pytest.mark.django_db


def test_project_str(project):
    assert str(project) == "31/12/2020 - Circularização de Estoque"


def test_project_date_display(project):
    assert project.date_display == "31/12/2020"
