"""Open-Meteo API request builder and response parser.

Planned: maps between domain concepts and Open-Meteo's JSON wire format.
Pydantic models with `extra="allow"` so new fields from Open-Meteo don't
break existing callers.
"""
