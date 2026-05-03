# open-meteo-client

A lightweight, async Python client for the [Open-Meteo](https://open-meteo.com) weather API — with high-level helpers that fit on a sticky note.

```python
from openmeteo import Location, UnitSystem, Forecast

location = Location(latitude=51.3, longitude=12.4, name="Dresden")
```

:::{admonition} Status: pre-alpha
:class: note

v0.0.6 ships domain layer building blocks: `Location`, `UnitSystem`, and `Forecast`. The full weather API (`Client`, `today()`, `forecast()`) lands in v0.1.0.

Track progress on the [roadmap board](https://github.com/users/jakobheine/projects/1).
:::

## What you want to read

This site follows the [Diátaxis](https://diataxis.fr/) framework — four
distinct kinds of documentation, each serving a different user intent:

```{list-table}
:header-rows: 1
:widths: 20 40 40

* - Section
  - When you need it
  - Example
* - [Tutorial](tutorial/getting-started.md)
  - "I'm new — walk me through my first call."
  - *Your first forecast in five lines*
* - [How-to guides](how-to/index.md)
  - "I have a specific goal."
  - *How do I handle rate limits?*
* - [Reference](reference/index.md)
  - "Just show me the exact API."
  - Every public function, class, and enum
* - [Explanation](explanation/index.md)
  - "Why is it designed that way?"
  - *Why async-only?*
```

## Install

```bash
pip install open-meteo-client
```

Requires Python 3.11+. Two runtime dependencies: [`httpx`](https://www.python-httpx.org/) and [`pydantic`](https://docs.pydantic.dev/).

## Contents

```{toctree}
:maxdepth: 2

tutorial/index
how-to/index
reference/index
explanation/index
```

---

## Elsewhere

**[📦 PyPI](https://pypi.org/project/open-meteo-client/)** ·
**[🐙 GitHub](https://github.com/jakobheine/open-meteo-client)** ·
**[💬 Discussions](https://github.com/jakobheine/open-meteo-client/discussions)** ·
**[🗺️ Roadmap](https://github.com/users/jakobheine/projects/1)**
