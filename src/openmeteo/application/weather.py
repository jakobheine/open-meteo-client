"""High-level convenience API.

Planned helpers:
    weather.today(location)       # current conditions by name or (lat, lon)
    weather.tomorrow(location)    # tomorrow's summary
    weather.forecast(location, days=7)

Sits on top of the `Client` class, handles geocoding, sensible defaults,
and human-friendly return shapes.
"""
