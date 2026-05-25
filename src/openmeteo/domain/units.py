"""Unit systems supported by the Open-Meteo client."""

from enum import StrEnum


class UnitSystem(StrEnum):
    """Unit presets accepted by high-level weather helpers."""

    METRIC = "metric"
    IMPERIAL = "imperial"


__all__ = ["UnitSystem"]
