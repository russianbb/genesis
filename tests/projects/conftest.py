import pytest

from .factories import ProjectFactory


@pytest.fixture(scope="function")
def project():
    return ProjectFactory()
