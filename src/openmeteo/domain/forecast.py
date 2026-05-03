"""Domain aggregate representing a weather forecast window."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from openmeteo.domain.location import Location


class Forecast(BaseModel):
    """Forecast aggregate for a location over a time window.

    Attributes:
        location: Forecast target location.
        start: Inclusive start timestamp.
        end: Exclusive end timestamp.
        temperatures_c: Ordered temperature values in Celsius.
    """

    model_config = ConfigDict(frozen=True)

    location: Location
    start: datetime
    end: datetime
    temperatures_c: tuple[float, ...]
