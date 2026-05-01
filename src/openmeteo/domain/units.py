"""Unit systems: metric (default) and imperial.

Planned: `UnitSystem` enum driving the `temperature_unit`, `wind_speed_unit`,
and `precipitation_unit` parameters on requests. Metric is default; callers
can override with `units="imperial"` on high-level helpers.
"""
