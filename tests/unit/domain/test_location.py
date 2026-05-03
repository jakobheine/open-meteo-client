"""Tests for Location domain primitive."""

import pytest

from openmeteo.domain.location import Location


def test_location_is_immutable_value_object() -> None:
    """Location should preserve coordinates and reject mutation."""
    location = Location(latitude=51.0504, longitude=13.7373, name="Dresden")

    assert location.latitude == 51.0504
    assert location.longitude == 13.7373
    assert location.name == "Dresden"

    with pytest.raises((AttributeError, ValueError)):
        location.latitude = 0.0  # type: ignore[misc]
