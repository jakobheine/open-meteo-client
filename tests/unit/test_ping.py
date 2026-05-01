"""Tests for `openmeteo.ping()`."""

import openmeteo


def test_ping_returns_string() -> None:
    """`ping()` returns a non-empty string."""
    result = openmeteo.ping()
    assert isinstance(result, str)
    assert result.strip() != ""


def test_ping_contains_version() -> None:
    """`ping()` includes the installed version so users can spot drift."""
    assert openmeteo.__version__ in openmeteo.ping()


def test_ping_does_not_raise() -> None:
    """`ping()` never raises; it's meant as a smoke test."""
    openmeteo.ping()  # no assertion; just verify no exception
