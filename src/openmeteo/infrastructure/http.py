"""HTTP transport adapter built on ``httpx.AsyncClient``."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self, cast

import httpx

from openmeteo._exceptions import ClientError, RateLimitError, TransportError

if TYPE_CHECKING:
    from types import TracebackType

DEFAULT_TIMEOUT_SECONDS = 10.0
HTTP_CLIENT_ERROR_MIN = 400
HTTP_SERVER_ERROR_MIN = 500

QueryParams = dict[str, str | int | float]
JsonObject = dict[str, object]


class HttpClient:
    """Small async JSON transport with Open-Meteo error mapping.

    Args:
        client: Optional ``httpx.AsyncClient`` to reuse. When omitted, this
            transport owns a client inside an async context manager.
        timeout: Per-request timeout in seconds for owned or ephemeral clients.
    """

    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        *,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        """Initialize the transport with an optional reusable client."""
        self._client = client
        self._timeout = timeout
        self._managed_client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Self:
        """Open an owned ``httpx.AsyncClient`` for multiple requests."""
        if self._client is None and self._managed_client is None:
            self._managed_client = httpx.AsyncClient(timeout=self._timeout)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the owned ``httpx.AsyncClient`` when the context exits."""
        if self._managed_client is not None:
            await self._managed_client.aclose()
            self._managed_client = None

    async def get_json(self, url: str, *, params: QueryParams | None = None) -> JsonObject:
        """Send a GET request and return a JSON object response.

        Args:
            url: Absolute URL to request.
            params: Query parameters for the request.

        Raises:
            ClientError: The request was rejected or returned non-object JSON.
            RateLimitError: Open-Meteo returned HTTP 429.
            TransportError: A network, timeout, or server error occurred.
        """
        client = self._active_client
        if client is not None:
            return await self._request_json(client, url, params=params)

        async with httpx.AsyncClient(timeout=self._timeout) as ephemeral_client:
            return await self._request_json(ephemeral_client, url, params=params)

    @property
    def _active_client(self) -> httpx.AsyncClient | None:
        return self._client or self._managed_client

    async def _request_json(
        self,
        client: httpx.AsyncClient,
        url: str,
        *,
        params: QueryParams | None,
    ) -> JsonObject:
        try:
            response = await client.get(url, params=params)
        except httpx.TimeoutException as exc:
            msg = "Open-Meteo request timed out"
            raise TransportError(msg) from exc
        except httpx.TransportError as exc:
            msg = "Open-Meteo request failed"
            raise TransportError(msg) from exc

        _raise_for_status(response)

        try:
            raw_payload: object = response.json()
        except ValueError as exc:
            msg = "Open-Meteo returned invalid JSON"
            raise TransportError(msg) from exc

        if not isinstance(raw_payload, dict):
            msg = "Open-Meteo returned JSON that was not an object"
            raise ClientError(msg)

        payload = cast("JsonObject", raw_payload)
        if payload.get("error") is True:
            reason = payload.get("reason")
            message = reason if isinstance(reason, str) else "Open-Meteo returned an error"
            raise ClientError(message)

        return payload


def _raise_for_status(response: httpx.Response) -> None:
    if response.status_code < HTTP_CLIENT_ERROR_MIN:
        return

    message = _status_error_message(response)
    if response.status_code == httpx.codes.TOO_MANY_REQUESTS:
        raise RateLimitError(message)
    if response.status_code < HTTP_SERVER_ERROR_MIN:
        raise ClientError(message)
    raise TransportError(message)


def _status_error_message(response: httpx.Response) -> str:
    try:
        raw_payload: object = response.json()
    except ValueError:
        raw_payload = None

    if isinstance(raw_payload, dict):
        reason = raw_payload.get("reason")
        if isinstance(reason, str) and reason:
            return reason

    return f"Open-Meteo request failed with HTTP {response.status_code}: {response.text}"


__all__ = ["HttpClient", "JsonObject", "QueryParams"]
