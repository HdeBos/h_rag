"""Shared fixtures for unit tests."""

import pytest
from pytest_mock import MockerFixture


@pytest.fixture()
def mock_config(mocker: MockerFixture):
    """Fixture to mock the get_config function with a dynamic return value."""

    def _mock(module_path: str, *keys: str, return_value: str) -> MockerFixture:
        return mocker.patch(
            f"{module_path}.get_config",
            side_effect=lambda *args: return_value if args == keys else None,
        )

    return _mock
