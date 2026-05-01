"""Live canary: weather.today('Dresden') against the real Open-Meteo API.

This test hits the real network. It's excluded from default `just test` runs
and picked up by the scheduled workflow.

Assertion philosophy (see tests/live/README.md):
- **Exact** assertions for things we control (lat, lon we send) or that
  are derived-but-stable (timezone)
- **Structural / existence** assertions for fields we expect Open-Meteo
  to return
- **Range** assertions for volatile values (temperature changes every hour)
"""

import pytest


@pytest.mark.live
@pytest.mark.not_implemented("openmeteo.today() is not implemented yet")
async def test_live_today_in_dresden() -> None:
    """`openmeteo.today('Dresden')` returns a sensible current forecast."""
    import openmeteo  # noqa: PLC0415  (import late so xfail bails before ModuleNotFoundError)

    result = await openmeteo.today("Dresden")

    # --- Exact / stable ---
    # Open-Meteo rounds lat/lon slightly; Dresden is ~51.05 N, 13.74 E.
    assert 51.0 < result.latitude < 51.1
    assert 13.7 < result.longitude < 13.8
    # Dresden is in the Berlin timezone and that's not going to change.
    assert result.timezone == "Europe/Berlin"

    # --- Structural / existence ---
    # The 'current' block is what today() is built on.
    assert result.current is not None
    assert isinstance(result.current.temperature_2m, float)
    assert isinstance(result.current.weather_code, int)

    # --- Sanity ranges (value changes hourly; just catch nonsense) ---
    assert -40 < result.current.temperature_2m < 50, (
        f"temperature {result.current.temperature_2m}°C out of plausible range"
    )
    assert 0 <= result.current.relative_humidity_2m <= 100
    assert 0 <= result.current.precipitation < 200
    assert 0 <= result.current.weather_code <= 100  # WMO codes live in [0, 100]
    assert 0 <= result.current.wind_speed_10m < 300  # km/h; tornados excepted
