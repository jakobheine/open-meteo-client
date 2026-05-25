"""Lightweight async Python client for the Open-Meteo weather API."""

__version__ = "0.1.0"

from openmeteo import application as application
from openmeteo.application import weather as weather
from openmeteo.application.client import OpenMeteoClient
from openmeteo.application.health import ping
from openmeteo.application.weather import today
from openmeteo.domain.forecast import CurrentWeather, Forecast
from openmeteo.domain.location import Location
from openmeteo.domain.variable import Variable

__all__ = [
    "CurrentWeather",
    "Forecast",
    "Location",
    "OpenMeteoClient",
    "Variable",
    "__version__",
    "application",
    "ping",
    "today",
    "weather",
]
