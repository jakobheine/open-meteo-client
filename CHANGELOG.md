# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Link to the public [Roadmap project board](https://github.com/users/jakobheine/projects/1)
  in the README.
- `AGENTS.md` — instructions for AI coding assistants working in the repo,
  following the [agents.md convention](https://agents.md/). Codifies tooling,
  conventions, release flow, and the two-dep + no-FlatBuffers policies so
  agents don't need to re-derive them each session.
- **Domain-Driven Design package skeleton** under `src/openmeteo/` with
  `domain/`, `application/`, and `infrastructure/` layers. Each module is
  a docstring-only placeholder for now. Layering rules documented in
  `AGENTS.md` and `CONTRIBUTING.md`.
- **Test-Driven Development support**: custom `@pytest.mark.not_implemented("reason")`
  marker (registered in `tests/conftest.py`) that translates to a strict
  `xfail`. Red tests pass CI while unimplemented; once they pass for real,
  CI fails with a prompt to remove the marker. Example in
  `tests/test_weather_today.py`.

## [0.0.3] - 2026-04-30

### Added
- README badges: CI, PyPI version, supported Python versions, license,
  Ruff, and all-contributors count.
- `CHANGELOG.md` following the Keep a Changelog convention.
- `CONTRIBUTING.md` with dev setup (uv + just), style guidelines, and
  commit message conventions.
- `.all-contributorsrc` + Contributors section in README following the
  [all-contributors](https://github.com/all-contributors/all-contributors)
  specification.
- Dependabot configuration (`.github/dependabot.yml`) for weekly Python
  and GitHub Actions dependency updates.
- Enabled GitHub Discussions for the repository.

### Changed
- Aligned project status between `pyproject.toml` and `README.md`: both
  now say "Planning". (The README previously said "Pre-alpha" while
  the classifier was still "1 - Planning".)

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

[Unreleased]: https://github.com/jakobheine/open-meteo-client/compare/v0.0.3...HEAD
[0.0.3]: https://github.com/jakobheine/open-meteo-client/releases/tag/v0.0.3
[0.0.2]: https://github.com/jakobheine/open-meteo-client/releases/tag/v0.0.2
[0.0.1]: https://github.com/jakobheine/open-meteo-client/releases/tag/v0.0.1
