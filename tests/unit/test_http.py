"""Tests for the HTTP transport adapter."""

import httpx
import pytest

from openmeteo._exceptions import ClientError, RateLimitError, TransportError
from openmeteo.infrastructure.http import HttpClient


async def test_get_json_returns_object_payload() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["name"] == "Dresden"
        return httpx.Response(200, json={"ok": True})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        result = await HttpClient(client=async_client).get_json(
            "https://example.test/weather",
            params={"name": "Dresden"},
        )

    assert result == {"ok": True}


async def test_http_client_context_manages_owned_client() -> None:
    client = HttpClient()

    async with client:
        pass


async def test_get_json_rejects_non_object_payload() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{"ok": True}])

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        with pytest.raises(ClientError, match="not an object"):
            await HttpClient(client=async_client).get_json("https://example.test/weather")


async def test_get_json_maps_invalid_json() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"{")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        with pytest.raises(TransportError, match="invalid JSON"):
            await HttpClient(client=async_client).get_json("https://example.test/weather")


async def test_get_json_raises_client_error_for_api_error_payload() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"error": True, "reason": "bad variable"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        with pytest.raises(ClientError, match="bad variable"):
            await HttpClient(client=async_client).get_json("https://example.test/weather")


async def test_get_json_maps_client_status() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, text="bad request")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        with pytest.raises(ClientError, match="HTTP 400"):
            await HttpClient(client=async_client).get_json("https://example.test/weather")


async def test_get_json_maps_rate_limit_status() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"reason": "slow down"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        with pytest.raises(RateLimitError, match="slow down"):
            await HttpClient(client=async_client).get_json("https://example.test/weather")


async def test_get_json_maps_server_status() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="unavailable")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        with pytest.raises(TransportError, match="HTTP 503"):
            await HttpClient(client=async_client).get_json("https://example.test/weather")


async def test_get_json_maps_timeout_errors() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        message = "timeout"
        raise httpx.ReadTimeout(message, request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        with pytest.raises(TransportError, match="timed out"):
            await HttpClient(client=async_client).get_json("https://example.test/weather")


async def test_get_json_maps_transport_errors() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        message = "boom"
        raise httpx.ConnectError(message, request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as async_client:
        with pytest.raises(TransportError, match="request failed"):
            await HttpClient(client=async_client).get_json("https://example.test/weather")
