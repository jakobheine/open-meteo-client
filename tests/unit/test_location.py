"""Tests for the Location value object."""

import pytest
from pydantic import ValidationError

from openmeteo.domain.location import Location


def test_location_strips_optional_text() -> None:
    location = Location(
        latitude=51.05,
        longitude=13.74,
        name=" Dresden ",
        timezone=" Europe/Berlin ",
        country_code=" DE ",
    )

    assert location.name == "Dresden"
    assert location.timezone == "Europe/Berlin"
    assert location.country_code == "DE"


def test_location_accepts_explicit_none_optional_text() -> None:
    location = Location(
        latitude=51.05,
        longitude=13.74,
        name=None,
        timezone=None,
        country_code=None,
    )

    assert location.name is None
    assert location.timezone is None
    assert location.country_code is None


def test_location_rejects_blank_optional_text() -> None:
    with pytest.raises(ValidationError):
        Location(latitude=51.05, longitude=13.74, name=" ")


def test_location_validates_latitude_bounds() -> None:
    with pytest.raises(ValidationError):
        Location(latitude=91, longitude=13.74)


def test_location_validates_longitude_bounds() -> None:
    with pytest.raises(ValidationError):
        Location(latitude=51.05, longitude=181)


def test_location_is_immutable() -> None:
    location = Location(latitude=51.05, longitude=13.74)

    with pytest.raises(ValidationError):
        # pyrefly: ignore [read-only]
        location.latitude = 52.0
