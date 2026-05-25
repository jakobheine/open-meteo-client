"""Exception hierarchy for open-meteo-client."""


class OpenMeteoError(Exception):
    """Base class for all errors raised by open-meteo-client."""


class ClientError(OpenMeteoError):
    """The request was invalid or Open-Meteo returned an unusable response."""


class LocationNotFoundError(ClientError):
    """A human-readable location name could not be resolved."""


class RateLimitError(ClientError):
    """Open-Meteo rejected the request because of rate limiting."""


class TransportError(OpenMeteoError):
    """A network, timeout, or server-side failure prevented the request."""


__all__ = [
    "ClientError",
    "LocationNotFoundError",
    "OpenMeteoError",
    "RateLimitError",
    "TransportError",
]
