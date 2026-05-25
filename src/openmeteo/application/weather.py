"""High-level convenience API for common weather use cases."""

from __future__ import annotations

from typing import TYPE_CHECKING

from openmeteo.application.client import OpenMeteoClient

if TYPE_CHECKING:
    from openmeteo.application.client import LocationInput
    from openmeteo.domain.forecast import Forecast


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
