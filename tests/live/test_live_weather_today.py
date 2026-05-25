"""Live canary: openmeteo.today('Dresden') against the real Open-Meteo API.

Excluded from default `just test` runs; picked up by the scheduled
`live.yml` workflow.

Assertion philosophy:

- **Stable fields** (lat, lon, timezone) — compare against the fixture
  with a small tolerance. If Open-Meteo starts returning different
  coordinates for Dresden, we want to know.
- **Structural existence** — any field in the fixture must also exist
  in the live response. Catches Open-Meteo deprecations automatically
  as long as we refresh the fixture periodically.
- **Volatile fields** (temperature, precipitation, wind, etc.) — check
  only that they're within absolute plausible ranges. Fixture values
  would be wrong half the year.
"""

import json
from pathlib import Path
from typing import Any

import pytest

FIXTURE_PATH = Path(__file__).parent.parent / "fixtures" / "today_dresden.json"
FIXTURE: dict[str, Any] = json.loads(FIXTURE_PATH.read_text())


@pytest.mark.live
async def test_live_today_in_dresden() -> None:
    """`openmeteo.today('Dresden')` returns a sensible current forecast."""
    import openmeteo  # noqa: PLC0415  (imported late so xfail bails cleanly)

    result = await openmeteo.today("Dresden")

    # --- Stable fields vs fixture (with small tolerance) ---
    assert result.latitude == pytest.approx(FIXTURE["latitude"], abs=0.1)
    assert result.longitude == pytest.approx(FIXTURE["longitude"], abs=0.1)
    assert result.timezone == FIXTURE["timezone"]

    # --- Structural: every field in the fixture must still exist ---
    current_dict = result.current.model_dump()
    fixture_current_fields = set(FIXTURE["current"].keys())
    missing = fixture_current_fields - set(current_dict.keys())
    assert not missing, (
        f"Fields present in the fixture but missing from the live response: {missing}. "
        f"Open-Meteo may have renamed or removed them."
    )

    # --- Volatile fields: absolute plausible ranges ---
    # Temperature in °C, plausible anywhere on Earth (Dresden: -40 to 50 is ample).
    assert -40 < result.current.temperature_2m < 50, (
        f"temperature {result.current.temperature_2m}°C out of plausible range"
    )
    assert 0 <= result.current.relative_humidity_2m <= 100
    assert 0 <= result.current.precipitation < 200  # mm in one observation interval
    assert 0 <= result.current.weather_code <= 100  # WMO codes live in [0, 100]
    assert 0 <= result.current.wind_speed_10m < 300  # km/h
