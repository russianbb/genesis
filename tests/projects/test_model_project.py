import pytest

pytestmark = pytest.mark.django_db


def test_project_str(project):
    assert str(project) == "31/01/1988 - Circularização de Estoque"


def test_project_date_display(project):
    assert project.date_display == "31/01/1988"


def test_project_date_display_dash(project):
    assert project.date_display_dash == "31-01-1988"


def test_project_status_display(project):
    assert project.status_display == "Ativo"


def test_project_company_str(project_company):
    expected_str = "31/01/1988 - Circularização de Estoque - Republica Jabuti LTDA ME"
    assert str(project_company) == expected_str


def test_project_initial_template(project):
    assert project.initial_email_template == "email/circularizacao/initial.html"


def test_project_email_from(project):
    assert project.email_from == "Onix Soluções Empresariais <projetos@onixse.com>"
