"""Lightweight async Python client for the Open-Meteo weather API.

This package is a pre-alpha release. Real functionality (``today``,
``tomorrow``, ``forecast``, ``Client``, ``Location``, ``Variable``) arrives
in v0.1.0. Until then, :func:`ping` exists so you can verify the package
imports and runs.

Track progress at https://github.com/jakobheine/open-meteo-client.
"""

__version__ = "0.0.6"

from openmeteo.application.health import ping

__all__ = ["__version__", "ping"]
