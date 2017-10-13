import pytest

from rest_framework.test import APIRequestFactory


@pytest.fixture()
def factory() -> APIRequestFactory:
    """APIRequestFactory instance."""

    return APIRequestFactory()
