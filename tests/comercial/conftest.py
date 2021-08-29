import pytest

from .factories import (
    CompanyFactory,
    CompanyFocalFactory,
    CompanyRtvFactory,
    FocalFactory,
    RtvFactory,
)


@pytest.fixture()
def focal():
    return FocalFactory()


@pytest.fixture()
def rtv():
    return RtvFactory()


@pytest.fixture()
def company(focal, rtv, user):
    company = CompanyFactory(designated=user)
    CompanyFocalFactory(company=company, focal=focal)
    CompanyRtvFactory(company=company, rtv=rtv)
    return company
