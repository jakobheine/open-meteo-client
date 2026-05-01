# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **`openmeteo.ping()`** — a tiny sync smoke-test function that returns
  `"open-meteo-client {version}: pong"`. Lets users verify the package
  is installed before the real API lands.
- **Documentation site** (Sphinx + `sphinx_rtd_theme` + `myst-parser` +
  `sphinx-autodoc-typehints`), organized per the Diátaxis framework:
  tutorial, how-to, reference (auto-generated from docstrings), and
  explanation. First content written: getting started, installation
  check how-to, and three explanations (async, two dependencies,
  architecture).
- **Read the Docs config** (`.readthedocs.yaml`) so pushes auto-build
  and deploy to `open-meteo-client.readthedocs.io`.
- `docs` optional dependency group (`sphinx`, `sphinx-rtd-theme`,
  `myst-parser`, `sphinx-autodoc-typehints`, `sphinx-autobuild`).
- `Documentation` URL in `pyproject.toml` project URLs so PyPI displays
  a 📘 link in the project sidebar.
- README docs badge, "Documentation" section linking all four Diátaxis
  quadrants.
- `just docs-build`, `just docs-serve`, `just docs-clean` recipes.
- CI job `docs` that builds the Sphinx site with `-W` so broken
  references break the build.

## [0.0.4] - 2026-05-01

### Added
- **`Variable` enum auto-generated from Open-Meteo's OpenAPI spec** via
  `just regen-variables`. 53 variables at time of generation. CI verifies
  the committed file is up to date (`generated` job).
- `scripts/regen_variables.py` — the codegen script.
- **Live canary workflow** (`.github/workflows/live.yml`) — runs live
  tests daily at 06:00 UTC plus on manual trigger; opens a GitHub issue
  (labeled `live-canary`, `bug`) if the scheduled run fails.
- **Fixture** `tests/fixtures/today_dresden.json` — captured real
  Open-Meteo response for Dresden, used by the integration test.
- **Live test** `tests/live/test_live_weather_today.py` — hits the real
  API, asserts exact values for stable fields (lat/lon/timezone),
  structural existence for current-block fields, and sane ranges for
  volatile values.
- **Integration test** `tests/integration/test_weather_today.py` — uses
  the fixture via `pytest-httpx` for deterministic exact-match asserts.
- Codecov integration (`.codecov.yml`, OIDC upload, README badge) with
  a 95% coverage target on both project and patch coverage.
- Monthly-downloads badge (pepy.tech) in the README.
- Link to the public [Roadmap project board](https://github.com/users/jakobheine/projects/1)
  in the README.
- `AGENTS.md` — instructions for AI coding assistants working in the repo,
  following the [agents.md convention](https://agents.md/).
- **Domain-Driven Design package skeleton** under `src/openmeteo/`
  (`domain/`, `application/`, `infrastructure/`) — docstring-only
  placeholders, layering rules documented.
- **Test-Driven Development support**: custom
  `@pytest.mark.not_implemented("reason")` marker translating to strict
  `xfail` (auto-cleanup once the code catches up).
- Runtime dependency on `httpx`.
- Dev dependencies: `pytest-httpx`, `pytest-rerunfailures`, `pyyaml`,
  `types-pyyaml`.
- Repo labels: `dependencies`, `ci`, `python`, `idea`, `design`,
  `v0.1.0`, `v0.2.0`, `live-canary`, `documentation`.

### Changed
- **Release pipeline now runs live tests before publish.** The
  `publish.yml` workflow is `build → live-check → publish`; if live
  tests fail, the `pypi` approval gate never appears and nothing is
  published.
- **Restructured test layout** into `tests/unit/`, `tests/integration/`,
  and `tests/live/` (with a README per tier). `just test` excludes live
  tests; new recipes `test-unit`, `test-integration`, `test-live`.
- `just test-live` retries each test up to 2 times with a 3s delay to
  tolerate transient network hiccups.
- Dropped the trivial `test_import`; version-check relaxed from
  exact-string match to PEP 440-shape check.
- CodeRabbit configured opt-in via `.coderabbit.yaml` (trigger with
  `@coderabbitai review` comment) to respect free-tier rate limits.
- Registered the `live` pytest marker in `conftest.py`.

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

[Unreleased]: https://github.com/jakobheine/open-meteo-client/compare/v0.0.4...HEAD
[0.0.4]: https://github.com/jakobheine/open-meteo-client/releases/tag/v0.0.4
[0.0.3]: https://github.com/jakobheine/open-meteo-client/releases/tag/v0.0.3
[0.0.2]: https://github.com/jakobheine/open-meteo-client/releases/tag/v0.0.2
[0.0.1]: https://github.com/jakobheine/open-meteo-client/releases/tag/v0.0.1
