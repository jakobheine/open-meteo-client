"""Tests for UnitSystem domain primitive."""

from openmeteo.domain.units import UnitSystem


def test_unit_system_values() -> None:
    """UnitSystem should expose stable public wire values."""
    assert UnitSystem.METRIC.value == "metric"
    assert UnitSystem.IMPERIAL.value == "imperial"
