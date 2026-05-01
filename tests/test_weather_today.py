"""Red tests describing the v0.1.0 high-level API.

These tests define the intended behavior of `openmeteo.weather.today(...)`
and friends. They are marked `not_implemented` and will pass as xfail
until the feature is built. Once implemented, remove the marker and the
test stays green.
"""

import pytest


@pytest.mark.not_implemented("weather.today() is not implemented yet")
def test_weather_today_returns_something_for_known_city() -> None:
    """`weather.today("Dresden")` returns a Forecast-like object with a
    non-None temperature for today."""
    # Delayed import: importing `weather` from openmeteo currently fails
    # because the module is just a docstring placeholder. Once implemented,
    # this will exercise the real code.
    from openmeteo.application import weather  # noqa: PLC0415  (explicit lazy)

    result = weather.today("Dresden")  # type: ignore[attr-defined]
    assert result is not None
    assert result.temperature is not None  # type: ignore[union-attr]
