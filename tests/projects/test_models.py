import pytest

pytestmark = pytest.mark.django_db


def test_project_str(project):
    assert str(project) == "31/12/2020 - Circularização de Estoque"


def test_project_date_display(project):
    assert project.date_display == "31/12/2020"


def test_project_status_display(project):
    assert project.status_display == "Ativo"


def test_project_company_str(project_company):
    expected_str = "31/12/2020 - Circularização de Estoque - Republica Jabuti LTDA ME"
    assert str(project_company) == expected_str
