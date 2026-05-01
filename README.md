# open-meteo-client

[![CI](https://github.com/jakobheine/open-meteo-client/actions/workflows/ci.yml/badge.svg)](https://github.com/jakobheine/open-meteo-client/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/jakobheine/open-meteo-client/graph/badge.svg)](https://codecov.io/gh/jakobheine/open-meteo-client)
[![PyPI version](https://img.shields.io/pypi/v/open-meteo-client.svg)](https://pypi.org/project/open-meteo-client/)
[![Python versions](https://img.shields.io/pypi/pyversions/open-meteo-client.svg)](https://pypi.org/project/open-meteo-client/)
[![Downloads](https://static.pepy.tech/badge/open-meteo-client/month)](https://pepy.tech/project/open-meteo-client)
[![License: Apache 2.0](https://img.shields.io/pypi/l/open-meteo-client.svg)](https://github.com/jakobheine/open-meteo-client/blob/main/LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

A lightweight, async Python client for the [Open-Meteo](https://open-meteo.com) weather API — with high-level helpers that fit on a sticky note.

```python
from openmeteo import weather

await weather.today("Dresden")
```

**Status:** 🚧 Planning — no code yet, just reserving the name and building the foundation. Track progress toward v0.1.0 in the [CHANGELOG](CHANGELOG.md).

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

## Roadmap

Public roadmap and backlog live on the [**Roadmap project board**](https://github.com/users/jakobheine/projects/1).
Pick anything from the Backlog column that's not claimed — see [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions and guidelines.

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://jakobheine.de/"><img src="https://avatars.githubusercontent.com/jakobheine?v=4?s=100" width="100px;" alt="Jakob Heine"/><br /><sub><b>Jakob Heine</b></sub></a><br /><a href="https://github.com/jakobheine/open-meteo-client/commits?author=jakobheine" title="Code">💻</a> <a href="https://github.com/jakobheine/open-meteo-client/commits?author=jakobheine" title="Documentation">📖</a> <a href="#design-jakobheine" title="Design">🎨</a> <a href="#infra-jakobheine" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#maintenance-jakobheine" title="Maintenance">🚧</a> <a href="https://github.com/jakobheine/open-meteo-client/commits?author=jakobheine" title="Tests">⚠️</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## License

Apache-2.0. See [LICENSE](LICENSE).
