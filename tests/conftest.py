import pytest

from rest_framework.test import APIRequestFactory


@pytest.fixture()
def factory():
    """APIRequestFactory instance."""

    return APIRequestFactory()
