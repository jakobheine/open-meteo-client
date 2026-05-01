# Getting started

:::{admonition} Pre-alpha caveat
:class: note

While v0.1.0 is in progress, the only thing you can actually do is call
[`ping()`](../reference/index.md). The snippets below that
use `today()` and friends are a preview of the intended API.
:::

## Install

```bash
pip install open-meteo-client
```

## Verify the install

```python
from openmeteo import ping

print(ping())
# -> "open-meteo-client 0.0.4: pong"
```

If that works, the package is healthy.

## (Preview, v0.1.0) Your first forecast in five lines

```python
import asyncio
from openmeteo import today  # arriving in v0.1.0

async def main() -> None:
    forecast = await today("Dresden")
    print(f"It's currently {forecast.current.temperature_2m}°C in Dresden.")

asyncio.run(main())
```

## What's next

- Browse the [How-to guides](../how-to/index.md) for specific tasks.
- See the full public API in the [Reference](../reference/index.md).
- Read [the design explanations](../explanation/index.md) if you care about
  the "why".
