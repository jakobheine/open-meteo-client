"""High-level convenience API for common weather use cases."""

from __future__ import annotations

from openmeteo.application.client import LocationInput, OpenMeteoClient
from openmeteo.domain.forecast import Forecast  # noqa: TC001


async def today(location: LocationInput) -> Forecast:
    """Return current weather for today at a location.

    Args:
        location: Place name, ``Location`` instance, or ``(latitude, longitude)`` tuple.

    Returns:
        A parsed domain ``Forecast`` with current weather conditions.
    """
    async with OpenMeteoClient() as client:
        return await client.today(location)


__all__ = ["today"]
