"""Domain aggregate representing a weather forecast window."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

    from openmeteo.domain.location import Location


@dataclass(frozen=True, slots=True)
class Forecast:
    """Forecast aggregate for a location over a time window.

    Attributes:
        location: Forecast target location.
        start: Inclusive start timestamp.
        end: Exclusive end timestamp.
        temperatures_c: Ordered temperature values in Celsius.
    """

    location: Location
    start: datetime
    end: datetime
    temperatures_c: list[float]
