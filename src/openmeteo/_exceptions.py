"""Exception hierarchy for open-meteo-client.

Planned taxonomy:
    OpenMeteoError          — base class
        ├── ClientError     — 4xx or our request is malformed
        │     ├── LocationNotFoundError
        │     └── RateLimitError
        └── TransportError  — network issues, timeouts, 5xx
"""
