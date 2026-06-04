"""Tests for supported unit systems."""

from openmeteo.domain.units import UnitSystem


def test_unit_system_values_are_public_api_strings() -> None:
    assert UnitSystem.METRIC == "metric"
    assert UnitSystem.IMPERIAL == "imperial"
