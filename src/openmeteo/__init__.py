"""Lightweight async Python client for the Open-Meteo weather API."""

__version__ = "0.0.6"

from openmeteo.application.health import ping
from openmeteo.domain import Forecast, Location, UnitSystem, Variable

__all__ = ["Forecast", "Location", "UnitSystem", "Variable", "__version__", "ping"]
