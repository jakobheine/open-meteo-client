"""Value object representing a geographical location."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Location(BaseModel):
    """A WGS84 location used for weather requests.

    Attributes:
        latitude: Latitude in decimal degrees, constrained to ``[-90, 90]``.
        longitude: Longitude in decimal degrees, constrained to ``[-180, 180]``.
        name: Optional human-readable place name.
        timezone: Optional IANA timezone for the location.
        country_code: Optional ISO 3166-1 alpha-2 country code.
    """

    model_config = ConfigDict(frozen=True)

    latitude: float = Field(ge=-90.0, le=90.0)
    longitude: float = Field(ge=-180.0, le=180.0)
    name: str | None = None
    timezone: str | None = None
    country_code: str | None = None

    @field_validator("name", "timezone", "country_code")
    @classmethod
    def _strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        if stripped == "":
            msg = "optional location text fields must not be blank"
            raise ValueError(msg)
        return stripped


__all__ = ["Location"]
