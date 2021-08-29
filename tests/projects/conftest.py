import pytest

from tests.comercial.factories import (
    CompanyFactory,
    CompanyFocalFactory,
    CompanyRtvFactory,
    FocalFactory,
    RtvFactory,
)

from .factories import ProjectCompanyFactory, ProjectFactory


@pytest.fixture()
def focal():
    return FocalFactory()


@pytest.fixture()
def rtv():
    return RtvFactory()


@pytest.fixture()
def company(focal, rtv, user):
    company = CompanyFactory(designated=user, system="siagri")
    CompanyFocalFactory(company=company, focal=focal)
    CompanyRtvFactory(company=company, rtv=rtv)
    return company


@pytest.fixture(scope="function")
def project():
    return ProjectFactory()


@pytest.fixture(scope="function")
def project_company(project, company):
    return ProjectCompanyFactory(project=project, company=company)
