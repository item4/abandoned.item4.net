import pytest

from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture()
def factory() -> APIRequestFactory:
    """APIRequestFactory instance."""

    return APIRequestFactory()


@pytest.fixture()
def client() -> APIClient:
    """APICllient instance. override pytest-django default."""

    return APIClient()
