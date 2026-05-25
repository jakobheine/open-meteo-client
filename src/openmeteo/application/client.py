"""Low-level async client for Open-Meteo endpoints."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable
from typing import TYPE_CHECKING, Self

from openmeteo.domain.location import Location
from openmeteo.domain.variable import Variable
from openmeteo.infrastructure import geocoding, openmeteo_api
from openmeteo.infrastructure.http import HttpClient

if TYPE_CHECKING:
    from types import TracebackType

    from openmeteo.domain.forecast import Forecast

COORDINATE_PAIR_LENGTH = 2

Coordinates = tuple[float, float]
LocationInput = str | Coordinates | Location

TODAY_VARIABLES = (
    Variable.TEMPERATURE_2M,
    Variable.RELATIVE_HUMIDITY_2M,
    Variable.PRECIPITATION,
    Variable.WEATHER_CODE,
    Variable.WIND_SPEED_10M,
)

Geocoder = Callable[[str], Awaitable[Location]]


class OpenMeteoClient:
    """Async client exposing low-level Open-Meteo operations.

    Args:
        http_client: Optional transport override, primarily useful for tests.
    """

    def __init__(self, *, http_client: HttpClient | None = None) -> None:
        """Initialize the client with an optional HTTP transport."""
        self._http_client = http_client or HttpClient()

    async def __aenter__(self) -> Self:
        """Open shared HTTP resources for multiple API calls."""
        await self._http_client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close shared HTTP resources."""
        await self._http_client.__aexit__(exc_type, exc, traceback)

    async def forecast(
        self,
        location: LocationInput,
        *,
        variables: Iterable[Variable] = TODAY_VARIABLES,
    ) -> Forecast:
        """Fetch current forecast data for a location.

        Args:
            location: Place name, ``Location`` instance, or ``(latitude, longitude)`` tuple.
            variables: Current weather variables to request.

        Returns:
            A parsed domain ``Forecast``.
        """
        resolved_location = await _resolve_location(location, self.geocode)
        return await openmeteo_api.fetch_forecast(
            self._http_client,
            resolved_location,
            variables=variables,
        )

    async def today(self, location: LocationInput) -> Forecast:
        """Fetch today's current weather for a location.

        Args:
            location: Place name, ``Location`` instance, or ``(latitude, longitude)`` tuple.

        Returns:
            A parsed domain ``Forecast`` with current weather conditions.
        """
        return await self.forecast(location, variables=TODAY_VARIABLES)

    async def geocode(self, name: str) -> Location:
        """Resolve a place name with Open-Meteo's geocoding API.

        Args:
            name: Human-readable place name.

        Returns:
            The first matching ``Location``.
        """
        return await geocoding.geocode(name, self._http_client)


async def _resolve_location(location: LocationInput, geocode: Geocoder) -> Location:
    if isinstance(location, Location):
        return location
    if isinstance(location, str):
        return await geocode(location)
    return _location_from_coordinates(location)


def _location_from_coordinates(coordinates: Coordinates) -> Location:
    if len(coordinates) != COORDINATE_PAIR_LENGTH:
        msg = "coordinate location input must be a (latitude, longitude) tuple"
        raise ValueError(msg)
    latitude, longitude = coordinates
    return Location(latitude=latitude, longitude=longitude)


__all__ = ["TODAY_VARIABLES", "LocationInput", "OpenMeteoClient"]
