# Integration tests

Tests that exercise the client or high-level helpers with **mocked HTTP**
via `pytest-httpx`. Verify that the pieces (domain + application +
infrastructure) work together without touching the real network.

**What belongs here:**
- `Client.forecast()` with mocked responses
- `weather.today()`, `weather.tomorrow()` with mocked responses
- Fixture-based tests using captured real JSON

**What does NOT belong here:**
- Pure domain tests (no mocking needed) → `../unit/`
- Tests that hit the real Open-Meteo API → `../live/`
