# open-meteo-client justfile
# Run `just` with no args to see the list of recipes.
#
# The project uses `uv` for all Python invocations.
# `just install` creates a .venv/ for the default interpreter;
# all "single-version" recipes (format, lint, types, test, check) run inside that venv.
# The `test-all` recipe creates isolated envs for each supported Python version.

# Default: show available recipes
default:
    @just --list

# ---------- Core dev loop ----------

# Format code and auto-fix lint issues
format:
    uv run ruff format .
    uv run ruff check --fix .

# Check formatting (no changes) — used by CI and `just check`
format-check:
    uv run ruff format --check .

# Lint code (no auto-fix)
lint:
    uv run ruff check .

# Run static type checking
types:
    uv run mypy src/

# Run tests on the current interpreter (uses .venv/ from `just install`).
# Runs unit + integration only; live tests are excluded by the -m filter.
test:
    uv run pytest -m "not live"

# Run just the unit tests (fastest; no mocks, no network)
test-unit:
    uv run pytest tests/unit

# Run just the integration tests (mocked httpx)
test-integration:
    uv run pytest tests/integration

# Run the live tests against the real Open-Meteo API. Excluded from the
# default `just test`; used by the nightly workflow and before releases.
# Uses pytest-rerunfailures so a single transient network hiccup doesn't
# fail the suite (retries each test up to 2 times).
test-live:
    uv run pytest -m live tests/live --reruns 2 --reruns-delay 3

# Run tests on all supported Python versions (3.11, 3.12, 3.13, 3.14).
# Skips live tests; use `just test-live` separately.
test-all:
    #!/usr/bin/env bash
    set -euo pipefail
    for v in 3.11 3.12 3.13 3.14; do
        echo ""
        echo "=== Python $v ==="
        uv run --isolated --python $v --extra dev pytest -m "not live"
    done

# Run the full pre-commit verification: format + lint + types + tests
check: format-check lint types test
    @echo ""
    @echo "✅ All checks passed"

# Same as check, but runs tests on all Python versions
check-all: format-check lint types test-all
    @echo ""
    @echo "✅ All checks passed on all Python versions"

# ---------- Build & release ----------

# Clean build artifacts
clean:
    rm -rf dist/ build/ *.egg-info src/*.egg-info
    rm -rf .ruff_cache .mypy_cache .pytest_cache
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Build wheel + sdist with Python 3.14
build: clean
    uv build --python 3.14

# Full release pipeline (does NOT upload — manual step after this)
release: check-all build
    @echo ""
    @echo "✅ Release artifacts ready in dist/"
    @ls -la dist/

# ---------- Setup ----------

# Install dev dependencies + this package in editable mode (creates .venv/)
install:
    uv sync --all-extras

# Install Python versions needed for test-all
install-pythons:
    uv python install 3.11 3.12 3.13 3.14

# ---------- Codegen ----------

# Regenerate src/openmeteo/_generated/variables.py from Open-Meteo's OpenAPI spec.
# Run this when the upstream spec changes and commit the result.
regen-variables:
    uv run python scripts/regen_variables.py

# Verify that the committed _generated files match what regeneration would produce.
# Used by CI; fails if someone edited a generated file by hand or forgot to regen.
check-generated:
    #!/usr/bin/env bash
    set -euo pipefail
    uv run python scripts/regen_variables.py
    if ! git diff --exit-code src/openmeteo/_generated/; then
        echo ""
        echo "❌ Generated files are out of date. Run 'just regen-variables' and commit."
        exit 1
    fi
    echo "✅ Generated files are up to date"

# ---------- Documentation ----------

# Build the Sphinx docs into docs/_build/html.
docs-build:
    uv run --extra docs sphinx-build -b html -W --keep-going docs docs/_build/html
    @echo ""
    @echo "✅ Docs built. Open docs/_build/html/index.html"

# Live preview the docs at http://localhost:8000 (auto-rebuilds on save).
docs-serve:
    uv run --extra docs sphinx-autobuild docs docs/_build/html --open-browser

# Remove the docs build output.
docs-clean:
    rm -rf docs/_build
