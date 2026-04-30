# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Project badges (CI, PyPI version, Python versions, License, Ruff) in `README.md`.
- `CHANGELOG.md` following the Keep a Changelog convention.

## [0.0.2] - 2026-04-30

### Changed
- Version bump to exercise the full release pipeline (CI, tagging,
  GitHub Release, and Trusted Publishing to PyPI). No functional changes —
  still a stub package.

## [0.0.1] - 2026-04-30

### Added
- Initial package stub to reserve the `open-meteo-client` name on PyPI.
- Project scaffold with `src/openmeteo/` layout.
- Apache-2.0 license (with NOTICE).
- `py.typed` marker for downstream type checkers.
- `pyproject.toml` (PEP 621) using `hatchling` as the build backend, with
  dynamic version sourced from `src/openmeteo/__init__.py`.
- Strict `ruff` + `mypy` configuration.
- `justfile` with `format`, `lint`, `types`, `test`, `test-all`, `check`,
  `check-all`, `build`, `release`, and `clean` recipes.
- GitHub Actions workflows:
  - `ci.yml` — lint/format/types + pytest matrix on Python 3.11–3.14
  - `publish.yml` — build and upload to PyPI via Trusted Publishing

[Unreleased]: https://github.com/jakobheine/open-meteo-client/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/jakobheine/open-meteo-client/releases/tag/v0.0.2
[0.0.1]: https://github.com/jakobheine/open-meteo-client/releases/tag/v0.0.1
