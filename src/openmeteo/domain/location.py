"""Value object representing a geographic location."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Location:
    """Immutable location value object.

    Attributes:
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.
        name: Optional human-readable location name.
    """

    latitude: float
    longitude: float
    name: str | None = None
