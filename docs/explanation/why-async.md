# Why async-only

`open-meteo-client` exposes an async public API and does not ship a
synchronous counterpart. Here's the reasoning.

## Async is the dominant style for new I/O code in 2026

- Modern HTTP libraries (`httpx`, `aiohttp`) are async-first.
- Frameworks that commonly consume weather data (FastAPI, Starlette,
  Home Assistant) are async throughout.
- Typed Python has excellent async ergonomics — `async def`,
  `async with`, context managers, cancellation.

## Sync is easy to add later if needed

`httpx` supports both sync and async with nearly identical APIs. If
real demand for a sync surface appears, we can add one without changing
the async one.

## Sync users today have an escape hatch

You can always run the async API from synchronous code:

```python
import asyncio
from openmeteo import ping

asyncio.run_in_executor  # not needed here — ping() is sync
```

Once `today()` lands:

```python
import asyncio
from openmeteo import today

forecast = asyncio.run(today("Dresden"))
```

One line of ceremony per call. Acceptable.

## The cost of shipping both

Two surfaces doubles the test matrix, the documentation, and the bug
reports. Until someone asks for sync, it's pure overhead.

## Decision

Async-only for v0.1.0. Revisit when either (a) real users ask for sync
or (b) we build something (like a CLI) that would benefit from a sync
entrypoint.
