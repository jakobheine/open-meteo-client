"""Domain models for weather forecasts."""

from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel, ConfigDict, Field

from openmeteo.domain.location import Location  # noqa: TC001


class CurrentWeather(BaseModel):
    """Current weather conditions at a forecast location.

    Attributes:
        time: Local observation time returned by Open-Meteo.
        interval: Observation interval in seconds.
        temperature_2m: Air temperature at 2 meters in degrees Celsius.
        relative_humidity_2m: Relative humidity at 2 meters in percent.
        precipitation: Precipitation amount in millimeters.
        weather_code: WMO weather interpretation code.
        wind_speed_10m: Wind speed at 10 meters in kilometers per hour.
    """

    model_config = ConfigDict(frozen=True)

    time: datetime
    interval: int = Field(ge=0)
    temperature_2m: float
    relative_humidity_2m: int = Field(ge=0, le=100)
    precipitation: float = Field(ge=0.0)
    weather_code: int = Field(ge=0)
    wind_speed_10m: float = Field(ge=0.0)


class Forecast(BaseModel):
    """A weather forecast for one resolved location.

    Attributes:
        location: Resolved forecast location.
        timezone: IANA timezone used for returned timestamps.
        current: Current weather conditions.
        timezone_abbreviation: Short timezone label returned by Open-Meteo.
        elevation: Elevation in meters.
        utc_offset_seconds: UTC offset of the returned timezone.
    """

    model_config = ConfigDict(frozen=True)

    location: Location
    timezone: str
    current: CurrentWeather
    timezone_abbreviation: str | None = None
    elevation: float | None = None
    utc_offset_seconds: int | None = None

    @property
    def latitude(self) -> float:
        """Return the forecast latitude in decimal degrees."""
        return self.location.latitude

    @property
    def longitude(self) -> float:
        """Return the forecast longitude in decimal degrees."""
        return self.location.longitude

    @property
    def name(self) -> str | None:
        """Return the resolved place name, if one is known."""
        return self.location.name


__all__ = ["CurrentWeather", "Forecast"]
