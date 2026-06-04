"""Geocoding adapter for resolving place names with Open-Meteo."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from openmeteo._exceptions import ClientError, LocationNotFoundError
from openmeteo.domain.location import Location
from openmeteo.infrastructure.http import HttpClient, JsonObject  # noqa: TC001

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


class _GeocodingResultPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    latitude: float
    longitude: float
    timezone: str | None = None
    country_code: str | None = None


class _GeocodingPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    results: list[_GeocodingResultPayload] = Field(default_factory=list)


async def geocode(name: str, http_client: HttpClient) -> Location:
    """Resolve a place name to a ``Location`` using Open-Meteo geocoding.

    Args:
        name: Human-readable place name, for example ``"Dresden"``.
        http_client: Shared HTTP transport.

    Raises:
        LocationNotFoundError: No matching place was returned.
        ClientError: The geocoding response was malformed.
    """
    query = name.strip()
    if query == "":
        msg = "location name must not be blank"
        raise LocationNotFoundError(msg)

    payload = await http_client.get_json(
        GEOCODING_URL,
        params={
            "name": query,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )
    return _parse_geocoding_payload(payload, query=query)


def _parse_geocoding_payload(payload: JsonObject, *, query: str) -> Location:
    try:
        parsed = _GeocodingPayload.model_validate(payload)
    except ValidationError as exc:
        msg = "Open-Meteo returned an unexpected geocoding response"
        raise ClientError(msg) from exc

    if not parsed.results:
        msg = f"could not resolve location: {query}"
        raise LocationNotFoundError(msg)

    result = parsed.results[0]
    return Location(
        latitude=result.latitude,
        longitude=result.longitude,
        name=result.name,
        timezone=result.timezone,
        country_code=result.country_code,
    )


__all__ = ["GEOCODING_URL", "geocode"]
