# open-meteo-client

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

## License

Apache-2.0. See [LICENSE](LICENSE).
