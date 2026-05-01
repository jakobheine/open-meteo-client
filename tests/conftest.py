"""Shared pytest configuration.

Registers the `not_implemented` marker used to signal TDD red tests that
describe future behavior. A test marked `not_implemented` is expected to
fail until someone implements the feature; once it passes, pytest will
turn it into a hard failure, prompting the author to remove the marker.

Usage:
    @pytest.mark.not_implemented("weather.today is not implemented yet")
    def test_weather_today_in_dresden() -> None:
        result = weather.today("Dresden")
        assert result.temperature is not None
"""

from __future__ import annotations

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers so --strict-markers doesn't complain."""
    config.addinivalue_line(
        "markers",
        "not_implemented(reason): TDD red test. Expected to fail until the "
        "feature is implemented. Passes turn into failures (strict xfail) "
        "to force removal of the marker once the code catches up.",
    )
    config.addinivalue_line(
        "markers",
        "live: hits the real Open-Meteo API. Excluded from the default test "
        "run; used by the nightly scheduled workflow and pre-release checks.",
    )


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Translate `@pytest.mark.not_implemented(reason)` into a strict xfail."""
    for item in items:
        marker = item.get_closest_marker("not_implemented")
        if marker is None:
            continue
        reason = marker.args[0] if marker.args else "not implemented yet"
        item.add_marker(pytest.mark.xfail(reason=reason, strict=True))
