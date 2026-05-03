"""Value object representing a geographic location."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Location(BaseModel):
    """Immutable location value object.

    Attributes:
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.
        name: Optional human-readable location name.
    """

    model_config = ConfigDict(frozen=True)

    latitude: float
    longitude: float
    name: str | None = None
