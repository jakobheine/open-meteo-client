# AGENTS.md

Instructions for AI coding assistants working in this repository.

This file follows the [AGENTS.md convention](https://agents.md/).
If you're a human, see [CONTRIBUTING.md](CONTRIBUTING.md) instead.

## Project

`open-meteo-client` is a lightweight, async Python client for the
[Open-Meteo](https://open-meteo.com) weather API, with a high-level
convenience layer (`weather.today("Dresden")`).

**Status:** Planning — no functional code yet. The v0.1.0 goal is a working
low-level `Client` plus a `weather.today()` helper.

## Tech stack

- **Python:** target `>=3.11`, develop on `3.14`
- **Runtime deps (strict two-dep policy):** `httpx`, `pydantic` v2
- **Build backend:** `hatchling`
- **Package manager:** `uv`
- **Lint + format:** `ruff` (max-strict, `select = ["ALL"]` with curated ignores)
- **Type check:** `mypy --strict` plus extra flags
- **Tests:** `pytest` + `pytest-asyncio`
- **Task runner:** `just`

## Project layout

The package follows a lightweight **Domain-Driven Design (DDD)** layering.
Dependencies flow inward: infrastructure can import domain, but domain
cannot import infrastructure.

```
src/openmeteo/
├── __init__.py              # re-exports public API
├── _exceptions.py           # error taxonomy
├── domain/                  # pure domain, no IO
│   ├── location.py          # Location value object
│   ├── forecast.py          # Forecast aggregate root
│   ├── variable.py          # Variable enum
│   └── units.py             # UnitSystem enum
├── application/             # orchestration / use cases
│   ├── client.py            # low-level Client class
│   └── weather.py           # high-level weather.today() helpers
└── infrastructure/          # external integrations
    ├── http.py              # httpx wrapper, retries, timeouts
    ├── geocoding.py         # string -> (lat, lon)
    └── openmeteo_api.py     # JSON <-> domain parsing

tests/                       # pytest suite
├── conftest.py              # registers @pytest.mark.not_implemented
├── test_smoke.py
└── test_weather_today.py    # example TDD red test
```

**Layering rules (enforced by review, not yet by tooling):**
- `domain/` imports nothing from this package.
- `application/` imports from `domain/` and `infrastructure/`.
- `infrastructure/` imports from `domain/` only.
- `__init__.py` re-exports from `application/`.

Flatten if a module grows beyond one clear purpose.

## Commands

Prefer `just` recipes over raw tool invocations:

```bash
just install         # create .venv/ and install dev deps
just format          # ruff format + auto-fix
just check           # format-check + lint + mypy + tests (fast, 3.14 only)
just check-all       # same, but tests on 3.11/3.12/3.13/3.14
just build           # build wheel + sdist with Python 3.14
just release         # check-all + build (does NOT upload)
```

Run `just` with no args for the full list.

## Rules for agents

### Must

- **Always run `just check` before claiming a task is done.** Nothing ships
  without lint, types, and tests passing.
- **Write the test first (TDD).** For any new public behavior, first add a
  test describing what it should do, marked `@pytest.mark.not_implemented("reason")`.
  Then implement until the test passes. Then remove the `not_implemented`
  marker. See "TDD workflow" below.
- **Respect the DDD layering.** Domain is pure; infrastructure talks to
  the outside world; application orchestrates. Never import infrastructure
  from domain. See "Project layout" above.
- **Write type annotations on all new code.** `mypy --strict` is enforced.
- **Use Python 3.11 syntax only.** Ruff and mypy are pinned to `target-version = "py311"`.
  Do not use 3.12+ features like `class Container[T]:` (PEP 695 generics) or
  `type X = ...` aliases.
- **Use `list[X]`, `dict[K, V]`, `X | None`, `X | Y`** — not `List`, `Dict`,
  `Optional`, `Union`. No `from typing import List` style.
- **Google-style docstrings** on all public functions, classes, and modules.
- **Async-first.** The public API is async. Don't add sync wrappers unless
  explicitly asked.
- **Sign-off commits.** Use `git commit -s`.
- **Conventional Commits** for messages: `feat:`, `fix:`, `docs:`, `chore:`,
  `ci:`, `refactor:`, `test:`.
- **Update `CHANGELOG.md`** under `[Unreleased]` for any user-visible change.
- **All changes via PRs.** `main` is protected — direct pushes are rejected.
  Branch naming: `feat/...`, `fix/...`, `docs/...`, `chore/...`, `ci/...`.

### Must not

- **Do not add runtime dependencies beyond `httpx` and `pydantic`.** The
  two-dep policy is core to the library's positioning. If you think a new
  dep is needed, propose it in an issue first.
- **Do not use `requests`, `aiohttp`, `flatbuffers`, `pandas`, `numpy`.**
- **Do not introduce FlatBuffers support.** We use JSON; this is a
  deliberate decision documented in `decisions.md` (in planning notes).
- **Do not add type runtime-checkers like `typeguard`.** Pydantic handles
  boundary validation; mypy handles static checks. No third layer.
- **Do not commit to `main` directly.** Use a feature branch + PR.
- **Do not bump the version except as part of a dedicated release commit.**
  See the release flow below.
- **Do not store secrets anywhere.** PyPI uploads use Trusted Publishing
  (OIDC); no API tokens should appear in workflows, env vars committed to
  the repo, or anywhere else.
- **Do not weaken the ruff or mypy configs** without explicit discussion.

## TDD workflow

We practice strict red-green-refactor with automatic cleanup enforcement.

### The ritual

1. **Add a test** describing the new behavior, marked `@pytest.mark.not_implemented("reason")`.
   The marker (defined in `tests/conftest.py`) translates to a strict xfail.
   ```python
   import pytest

   @pytest.mark.not_implemented("weather.today() is not implemented yet")
   def test_weather_today_returns_current_temperature() -> None:
       from openmeteo.application import weather
       result = weather.today("Dresden")
       assert result.temperature is not None
   ```
2. **Run `just check`.** The test fails (as intended); pytest reports
   `XFAIL` and CI stays green.
3. **Implement the behavior** in the appropriate layer (usually domain +
   application).
4. **Run `just check` again.** The test now passes. With `strict=True`,
   pytest reports it as `XPASS` and **fails the test run** with a message
   like `[XPASS(strict)] weather.today() is not implemented yet`.
5. **Remove the `@pytest.mark.not_implemented(...)` marker.** The test
   should now run as a normal passing test. Commit.

### Why this works

- Writing the test first forces you to think about the API before the
  implementation.
- `strict=True` means the marker cannot silently rot — the moment the
  test passes, CI forces you to remove the marker.
- No CI is "red on purpose"; TDD red tests live as xfail, not failure.

### When `not_implemented` is NOT appropriate

- **Behavior that should never work** — use `pytest.raises(NotImplementedError)` or
  a regular assertion. Don't mark passing-by-failing as xfail.
- **External dependencies that may be down** — use `@pytest.mark.skipif(...)` instead.
- **Flaky tests** — fix the flakiness; don't hide it behind a marker.

## DDD layering rules

- **`domain/`** — pure. Value objects, aggregates, enums. Safe to use in
  any context (sync, async, tests, notebooks). Imports no other layer of
  this package.
- **`application/`** — orchestration. `Client`, high-level helpers.
  Depends on `domain/` and `infrastructure/`.
- **`infrastructure/`** — IO. HTTP client, retries, JSON parsing, geocoding.
  Depends on `domain/` only.
- **Package root (`__init__.py`)** — re-exports the public API from
  `application/` so users can write `from openmeteo import weather`
  without knowing the internal structure.

When in doubt, ask: *"If I removed the network, would this still make
sense?"* If yes, it's probably domain. If no, it's infrastructure.

## Conventions

### Code style
- Line length: **100 characters**
- Double quotes for strings
- One class per file when practical
- New file if a module exceeds ~400 lines

### Imports
- Prefer module-level imports (`import typing` + `typing.Any`) over
  name-level (`from typing import Any`) when it improves call-site clarity.
- One import per line.

### Error handling
- Fail fast, return early, keep nesting shallow.
- Specific exceptions over bare `except:`.

### Tests
- Put tests in `tests/`, named `test_*.py`.
- Async tests use `pytest-asyncio`; `asyncio_mode = "auto"` so the
  `@pytest.mark.asyncio` decorator is not needed.
- Tests get lighter ruff rules (no mandatory docstrings, `assert` is fine).

## Release flow

```bash
# 1. Bump version in src/openmeteo/__init__.py
# 2. Bump matching assertion in tests/test_smoke.py
# 3. Move CHANGELOG [Unreleased] entries into a dated [X.Y.Z] section
# 4. Commit + push via PR
# 5. After merge to main:
git tag vX.Y.Z
git push --tags
gh release create vX.Y.Z --generate-notes --title "vX.Y.Z"
# 6. The publish workflow triggers and waits for manual approval in the
#    'pypi' GitHub Environment. A human must click "Approve and deploy".
#    Do not bypass this approval gate.
```

## Where to look

- **Implementation decisions / "why" context:** `decisions.md` in the
  author's private planning notes (not in this repo; ask the maintainer if
  clarification is needed on a design choice).
- **User-facing docs:** `README.md`
- **Contribution process for humans:** `CONTRIBUTING.md`
- **What changed between versions:** `CHANGELOG.md`
- **Public API surface:** `src/openmeteo/__init__.py` (currently just exposes
  `__version__`; will re-export the intended public API once it exists)

## Code review

- **CodeRabbit** is installed but **opt-in** to respect free-tier rate limits
  (1 review per hour). To request a review, comment on the PR:
  - `@coderabbitai review` — review changes since last review
  - `@coderabbitai full review` — review from scratch
- Use it on meaningful code PRs, not docs/infra tweaks where ruff + mypy
  already cover the ground.

## When unsure

Stop and ask. Small, focused PRs with questions are better than large PRs
guessing at intent. Open a [Discussion](https://github.com/jakobheine/open-meteo-client/discussions)
or a draft PR.
