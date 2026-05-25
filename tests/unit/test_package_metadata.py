"""Tests for package-level metadata (`__version__`, exposed API surface).

Catches issues like a release where `__init__.py` and `pyproject.toml`
drift apart, or an accidental removal of a public name from the top-level
package.
"""

import openmeteo


def test_version_is_a_string() -> None:
    """`openmeteo.__version__` should be a string matching PEP 440."""
    assert isinstance(openmeteo.__version__, str)
    assert len(openmeteo.__version__) > 0
    # crude PEP 440 check — three dot-separated segments, digits-ish
    parts = openmeteo.__version__.split(".")
    assert len(parts) >= 3, f"expected X.Y.Z, got {openmeteo.__version__!r}"


def test_public_weather_api_is_exported() -> None:
    assert openmeteo.today is openmeteo.weather.today
    assert openmeteo.OpenMeteoClient.__name__ == "OpenMeteoClient"
    assert openmeteo.Forecast.__name__ == "Forecast"
    assert openmeteo.Location.__name__ == "Location"
