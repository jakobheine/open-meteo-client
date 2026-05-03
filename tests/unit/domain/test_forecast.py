"""Tests for Forecast domain primitive."""

from datetime import UTC, datetime

import openmeteo
from openmeteo.domain.forecast import Forecast
from openmeteo.domain.location import Location


def test_forecast_holds_time_window_and_temperature() -> None:
    """Forecast should model a time window and temperature points."""
    start = datetime(2026, 1, 1, tzinfo=UTC)
    end = datetime(2026, 1, 1, 1, tzinfo=UTC)

    forecast = Forecast(
        location=Location(latitude=51.0504, longitude=13.7373, name="Dresden"),
        start=start,
        end=end,
        temperatures_c=(3.2, 3.5),
    )

    assert forecast.location.name == "Dresden"
    assert forecast.start == start
    assert forecast.end == end
    assert forecast.temperatures_c == (3.2, 3.5)


def test_public_exports_include_domain_primitives() -> None:
    """Top-level package should re-export domain primitives for users."""
    assert hasattr(openmeteo, "Location")
    assert hasattr(openmeteo, "Forecast")
    assert hasattr(openmeteo, "UnitSystem")
