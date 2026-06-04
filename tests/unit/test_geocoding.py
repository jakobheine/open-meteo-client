"""Tests for the Open-Meteo geocoding adapter."""

import httpx
import pytest

from openmeteo._exceptions import ClientError, LocationNotFoundError
from openmeteo.infrastructure.geocoding import GEOCODING_URL, geocode
from openmeteo.infrastructure.http import HttpClient


async def test_geocode_returns_first_result() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url).startswith(GEOCODING_URL)
        assert request.url.params["name"] == "Dresden"
        assert request.url.params["count"] == "1"
        return httpx.Response(
            200,
            json={
                "results": [
                    {
                        "name": "Dresden",
                        "latitude": 51.05089,
                        "longitude": 13.73832,
                        "timezone": "Europe/Berlin",
                        "country_code": "DE",
                    }
                ],
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        result = await geocode(" Dresden ", HttpClient(client=async_client))

    assert result.name == "Dresden"
    assert result.latitude == 51.05089
    assert result.longitude == 13.73832
    assert result.timezone == "Europe/Berlin"
    assert result.country_code == "DE"


async def test_geocode_rejects_blank_names() -> None:
    with pytest.raises(LocationNotFoundError, match="must not be blank"):
        await geocode(" ", HttpClient())


async def test_geocode_raises_when_no_results_match() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"results": []})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        with pytest.raises(LocationNotFoundError, match="could not resolve"):
            await geocode("Nowhere", HttpClient(client=async_client))


async def test_geocode_raises_on_malformed_payload() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"results": [{"name": "Dresden"}]})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        with pytest.raises(ClientError, match="unexpected geocoding"):
            await geocode("Dresden", HttpClient(client=async_client))
