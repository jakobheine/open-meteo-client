"""Lightweight self-check helpers.

This module exists so you can verify `open-meteo-client` is installed
and importable, before the real weather API (`today`, `tomorrow`,
`forecast`) lands in v0.1.0.
"""

from openmeteo import __version__ as _version


def ping() -> str:
    """Return a small string confirming the package is alive.

    Use this as a smoke test after installing, or in an automation to
    check that `open-meteo-client` is importable in your environment.
    It performs no I/O and never raises.

    Returns:
        A short human-readable string containing the installed version,
        e.g. ``"open-meteo-client 0.0.4: pong"``.

    Example:
        >>> from openmeteo import ping
        >>> ping()
        'open-meteo-client 0.0.4: pong'
    """
    return f"open-meteo-client {_version}: pong"
