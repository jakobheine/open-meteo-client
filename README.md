# open-meteo-client

[![CI](https://github.com/jakobheine/open-meteo-client/actions/workflows/ci.yml/badge.svg)](https://github.com/jakobheine/open-meteo-client/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/open-meteo-client.svg)](https://pypi.org/project/open-meteo-client/)
[![Python versions](https://img.shields.io/pypi/pyversions/open-meteo-client.svg)](https://pypi.org/project/open-meteo-client/)
[![License: Apache 2.0](https://img.shields.io/pypi/l/open-meteo-client.svg)](https://github.com/jakobheine/open-meteo-client/blob/main/LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A lightweight, async Python client for the [Open-Meteo](https://open-meteo.com) weather API — with high-level helpers that fit on a sticky note.

```python
from openmeteo import weather

await weather.today("Dresden")
```

**Status:** 🚧 Pre-alpha. Design in progress, not yet functional.

## Planned features

- **Lightweight** — two dependencies (`httpx`, `pydantic`), no FlatBuffers, no pandas
- **Async-first** — built on `httpx.AsyncClient`
- **Typed** — full pydantic v2 models, `StrEnum` for weather variables, IDE autocomplete
- **Two layers** — high-level convenience API (`weather.today()`) on top of a full low-level `Client`

## Install

```bash
pip install open-meteo-client
```

> ⚠️ Package reserved — no functionality yet. Check back for v0.1.0.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## License

Apache-2.0. See [LICENSE](LICENSE).
