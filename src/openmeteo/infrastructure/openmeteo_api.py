"""Open-Meteo forecast request builder and response parser."""

from __future__ import annotations

from collections.abc import Iterable  # noqa: TC003
from datetime import datetime  # noqa: TC003

from pydantic import BaseModel, ConfigDict, ValidationError

from openmeteo._exceptions import ClientError
from openmeteo.domain.forecast import CurrentWeather, Forecast
from openmeteo.domain.location import Location
from openmeteo.domain.variable import Variable  # noqa: TC001
from openmeteo.infrastructure.http import HttpClient, JsonObject, QueryParams  # noqa: TC001

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class _CurrentWeatherPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    time: datetime
    interval: int
    temperature_2m: float
    relative_humidity_2m: int
    precipitation: float
    weather_code: int
    wind_speed_10m: float


class _ForecastPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    latitude: float
    longitude: float
    timezone: str
    current: _CurrentWeatherPayload
    timezone_abbreviation: str | None = None
    elevation: float | None = None
    utc_offset_seconds: int | None = None


async def fetch_forecast(
    http_client: HttpClient,
    location: Location,
    *,
    variables: Iterable[Variable],
) -> Forecast:
    """Fetch and parse a forecast for a resolved location.

    Args:
        http_client: Shared HTTP transport.
        location: Resolved forecast location.
        variables: Current weather variables to request.

    Returns:
        A domain ``Forecast`` parsed from Open-Meteo JSON.
    """
    payload = await http_client.get_json(
        FORECAST_URL,
        params=_forecast_params(location, variables),
    )
    return parse_forecast(payload, requested_location=location)


def parse_forecast(payload: JsonObject, *, requested_location: Location) -> Forecast:
    """Parse an Open-Meteo forecast JSON object into a domain ``Forecast``.

    Args:
        payload: Raw JSON object returned by the forecast endpoint.
        requested_location: The location used to make the request.

    Raises:
        ClientError: The response does not match the expected forecast shape.
    """
    try:
        parsed = _ForecastPayload.model_validate(payload)
    except ValidationError as exc:
        msg = "Open-Meteo returned an unexpected forecast response"
        raise ClientError(msg) from exc

    forecast_location = Location(
        latitude=parsed.latitude,
        longitude=parsed.longitude,
        name=requested_location.name,
        timezone=parsed.timezone,
        country_code=requested_location.country_code,
    )
    return Forecast(
        location=forecast_location,
        timezone=parsed.timezone,
        timezone_abbreviation=parsed.timezone_abbreviation,
        elevation=parsed.elevation,
        utc_offset_seconds=parsed.utc_offset_seconds,
        current=CurrentWeather(
            time=parsed.current.time,
            interval=parsed.current.interval,
            temperature_2m=parsed.current.temperature_2m,
            relative_humidity_2m=parsed.current.relative_humidity_2m,
            precipitation=parsed.current.precipitation,
            weather_code=parsed.current.weather_code,
            wind_speed_10m=parsed.current.wind_speed_10m,
        ),
    )


def _forecast_params(location: Location, variables: Iterable[Variable]) -> QueryParams:
    current_variables = ",".join(variable.value for variable in variables)
    if current_variables == "":
        msg = "at least one current weather variable is required"
        raise ClientError(msg)

    return {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current": current_variables,
        "timezone": "auto",
    }


__all__ = ["FORECAST_URL", "fetch_forecast", "parse_forecast"]
