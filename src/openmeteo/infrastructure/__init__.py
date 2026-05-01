"""Infrastructure layer — external integrations.

Everything that touches the outside world: HTTP via `httpx`, JSON parsing,
retries, backoff, geocoding. Implements ports described by the application
layer; depends on domain types but never the other way around.
"""
