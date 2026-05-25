"""Tests for application-level location handling."""

import pytest

from openmeteo.application.client import _resolve_location
from openmeteo.domain.location import Location


async def test_resolve_location_returns_location_instances_unchanged() -> None:
    location = Location(latitude=51.05, longitude=13.74, name="Dresden")

    async def geocode(name: str) -> Location:
        pytest.fail(f"geocode should not be called for {name}")

    assert await _resolve_location(location, geocode) == location


async def test_resolve_location_geocodes_names() -> None:
    async def geocode(name: str) -> Location:
        assert name == "Dresden"
        return Location(latitude=51.05, longitude=13.74, name=name)

    result = await _resolve_location("Dresden", geocode)

    assert result.name == "Dresden"
    assert result.latitude == 51.05
    assert result.longitude == 13.74


async def test_resolve_location_accepts_coordinate_tuple() -> None:
    async def geocode(name: str) -> Location:
        pytest.fail(f"geocode should not be called for {name}")

    result = await _resolve_location((51.05, 13.74), geocode)

    assert result.latitude == 51.05
    assert result.longitude == 13.74
    assert result.name is None


async def test_resolve_location_rejects_invalid_coordinate_tuple() -> None:
    async def geocode(name: str) -> Location:
        pytest.fail(f"geocode should not be called for {name}")

    with pytest.raises(ValueError, match="coordinate"):
        # pyrefly: ignore [bad-argument-type]
        await _resolve_location((51.05,), geocode)
