"""Tests for Open-Meteo forecast parsing."""

import json
from pathlib import Path

import pytest

from openmeteo._exceptions import ClientError
from openmeteo.domain.location import Location
from openmeteo.domain.variable import Variable
from openmeteo.infrastructure.openmeteo_api import _forecast_params, parse_forecast

FIXTURE = Path(__file__).parent.parent / "fixtures" / "today_dresden.json"


def test_parse_forecast_maps_fixture_to_domain_model() -> None:
    payload = json.loads(FIXTURE.read_text())
    requested_location = Location(
        latitude=51.05089,
        longitude=13.73832,
        name="Dresden",
        country_code="DE",
    )

    forecast = parse_forecast(payload, requested_location=requested_location)

    assert forecast.name == "Dresden"
    assert forecast.latitude == payload["latitude"]
    assert forecast.longitude == payload["longitude"]
    assert forecast.location.country_code == "DE"
    assert forecast.current.temperature_2m == payload["current"]["temperature_2m"]


def test_parse_forecast_raises_for_malformed_payload() -> None:
    with pytest.raises(ClientError, match="unexpected forecast"):
        parse_forecast({}, requested_location=Location(latitude=51.05, longitude=13.74))


def test_forecast_params_include_location_and_current_variables() -> None:
    params = _forecast_params(
        Location(latitude=51.05, longitude=13.74),
        [Variable.TEMPERATURE_2M, Variable.WIND_SPEED_10M],
    )

    assert params == {
        "latitude": 51.05,
        "longitude": 13.74,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto",
    }


def test_forecast_params_require_at_least_one_variable() -> None:
    with pytest.raises(ClientError, match="at least one"):
        _forecast_params(Location(latitude=51.05, longitude=13.74), [])
