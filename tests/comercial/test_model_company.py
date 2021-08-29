import pytest

pytestmark = pytest.mark.django_db


def test_company_str(company):
    assert str(company) == "Republica Jabuti LTDA ME"


def test_company_email_to(company, focal):
    assert company.email_to == [focal.email]


def test_company_email_cc(company, rtv, user):
    assert company.email_cc == [rtv.email, "anderson.mercadante@onixse.com", user.email]
