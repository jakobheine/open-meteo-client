"""Integration test: `openmeteo.today('Dresden')` with a mocked HTTP layer.

Unlike the live test (which exercises the real API and allows value
ranges), this test feeds a frozen JSON fixture into httpx via
`pytest-httpx`, then asserts the **exact** parsed output. Deterministic.

If Open-Meteo changes their response shape and our fixture falls out of
date, the live test will catch it first; we then update the fixture and
revisit this test's expected values.
"""

import json
from pathlib import Path

import pytest
from pytest_httpx import HTTPXMock

FIXTURE = Path(__file__).parent.parent / "fixtures" / "today_dresden.json"


@pytest.mark.not_implemented("openmeteo.today() is not implemented yet")
async def test_today_in_dresden_parses_fixture(httpx_mock: HTTPXMock) -> None:
    """Given Open-Meteo's real response for Dresden, parse it exactly."""
    # Arrange: serve the fixture for any matching forecast request
    fixture_data = json.loads(FIXTURE.read_text())
    httpx_mock.add_response(
        url="https://api.open-meteo.com/v1/forecast",
        match_content=None,  # match regardless of query string for now
        json=fixture_data,
    )

    # Act
    import openmeteo  # noqa: PLC0415  (import late so xfail bails cleanly)

    result = await openmeteo.today("Dresden")

    # Assert — exact values from the fixture
    assert result.latitude == fixture_data["latitude"]
    assert result.longitude == fixture_data["longitude"]
    assert result.timezone == fixture_data["timezone"]

    current = fixture_data["current"]
    assert result.current.temperature_2m == current["temperature_2m"]
    assert result.current.relative_humidity_2m == current["relative_humidity_2m"]
    assert result.current.precipitation == current["precipitation"]
    assert result.current.weather_code == current["weather_code"]
    assert result.current.wind_speed_10m == current["wind_speed_10m"]
