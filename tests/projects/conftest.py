import pytest

from .factories import ProjectCompanyFactory, ProjectFactory


@pytest.fixture(scope="function")
def project():
    return ProjectFactory()


@pytest.fixture(scope="function")
def project_company():
    return ProjectCompanyFactory()
