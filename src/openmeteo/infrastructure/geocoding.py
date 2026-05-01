"""Geocoding adapter: resolve a place name to (lat, lon).

Planned: uses Open-Meteo's geocoding API. Results are cached in-process
for the lifetime of a `Client` to avoid redundant lookups for repeated
calls like `weather.today("Dresden")`.
"""
