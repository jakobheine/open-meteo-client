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

# Run tests on the current interpreter (uses .venv/ from `just install`)
test:
    uv run pytest

# Run tests on all supported Python versions (3.11, 3.12, 3.13, 3.14)
test-all:
    #!/usr/bin/env bash
    set -euo pipefail
    for v in 3.11 3.12 3.13 3.14; do
        echo ""
        echo "=== Python $v ==="
        uv run --isolated --python $v --extra dev pytest
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
