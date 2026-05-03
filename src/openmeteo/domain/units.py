"""Unit system enum used by weather queries."""

from __future__ import annotations

from enum import StrEnum


class UnitSystem(StrEnum):
    """Supported unit systems for weather data requests."""

    METRIC = "metric"
    IMPERIAL = "imperial"
