# open-meteo-client

A lightweight, async Python client for the [Open-Meteo](https://open-meteo.com) weather API — with high-level helpers that fit on a sticky note.

```python
from openmeteo import ping

print(ping())
# -> "open-meteo-client 0.0.4: pong"
```

:::{admonition} Status: planning
:class: warning

This package is pre-alpha. The real weather API (`today`, `tomorrow`,
`forecast`, `OpenMeteoClient`, `Location`) lands in v0.1.0. Until then, [`ping()`](reference/index.md)
exists so you can verify the package imports and runs.

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
