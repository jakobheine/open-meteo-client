"""Sanity test for the stub package."""

import openmeteo


def test_import() -> None:
    """The package should be importable."""
    assert openmeteo is not None


def test_version() -> None:
    """The package should expose a version string."""
    assert isinstance(openmeteo.__version__, str)
    assert openmeteo.__version__ == "0.0.1"
