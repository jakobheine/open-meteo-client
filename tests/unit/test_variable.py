"""Tests for the auto-generated Variable enum."""

from openmeteo.domain.variable import Variable


def test_variable_is_str_enum() -> None:
    """`Variable` values should be usable anywhere a string is expected."""
    assert Variable.TEMPERATURE_2M == "temperature_2m"
    assert Variable.PRECIPITATION == "precipitation"


def test_variable_has_expected_members() -> None:
    """Spot-check a handful of members that should always be in the spec."""
    expected = {
        "TEMPERATURE_2M",
        "PRECIPITATION",
        "WIND_SPEED_10M",
        "CLOUD_COVER",
        "WEATHER_CODE",
    }
    actual = {m.name for m in Variable}
    missing = expected - actual
    assert not missing, f"missing expected variables: {missing}"


def test_variable_name_roundtrip() -> None:
    """Enum members map back to valid upstream identifiers."""
    for member in Variable:
        # All values are snake_case ASCII, no uppercase, no spaces
        assert member.value == member.value.lower()
        assert " " not in member.value
        assert all(c.isalnum() or c == "_" for c in member.value)
