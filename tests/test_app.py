import pytest

pytestmark = pytest.mark.django_db


def test_01_conftest(hello):
    assert hello == "hello"
