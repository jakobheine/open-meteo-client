# Contributing to open-meteo-client

Thanks for your interest in contributing! This project is a hobby, but I'm
happy to review PRs and discuss ideas. Small, focused contributions are
easier to review than sweeping refactors.

## Ways to help

- **Report a bug** — open an issue
- **Request a feature** — open an issue or start a discussion
- **Improve documentation** — typos, examples, clarifications all welcome
- **Submit a PR** — bug fixes, small enhancements, new features

If you're unsure whether a change is a good fit, **open a discussion or
issue first** before writing code.

## Development setup

You need:

- **[uv](https://docs.astral.sh/uv/)** — Python and dependency management
- **[just](https://just.systems/)** — task runner
- Git

### First-time setup

```bash
git clone https://github.com/jakobheine/open-meteo-client.git
cd open-meteo-client
just install              # creates .venv/ and installs dev dependencies
just install-pythons      # installs Python 3.11/3.12/3.13/3.14 via uv
```

### Daily dev loop

```bash
just format               # auto-format + auto-fix lint issues
just check                # fast: format-check + lint + mypy + tests (on 3.14)
just check-all            # full: same, plus tests on all Python versions
```

### Available recipes

Run `just` with no args to see all available recipes:

```bash
just
```

## Style and conventions

- **Python:** 3.11+ syntax only (we develop on 3.14 but target 3.11+).
  `ruff` and `mypy` enforce this.
- **Line length:** 100 characters
- **Formatter:** `ruff format` (no need to think about it — just run `just format`)
- **Types:** required everywhere, enforced by `mypy --strict`
- **Docstrings:** Google style, required on public API
- **Tests:** pytest, async tests supported (`pytest-asyncio`)

## Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>
```

Common types:
- `feat:` — new user-facing feature
- `fix:` — bug fix
- `docs:` — documentation only
- `refactor:` — code change that's neither a feature nor a fix
- `test:` — adding or adjusting tests
- `chore:` — maintenance, tooling, build
- `ci:` — changes to CI workflows

Examples:
```
feat(weather): add weather.tomorrow(location) helper
fix(client): handle 429 rate-limit responses with backoff
docs: add usage example for timezone parameter
```

Please **sign off** your commits (`git commit -s`).

## Pull request process

1. **Fork** the repo, create a feature branch (`git checkout -b feat/my-thing`).
2. **Make your change** and run `just check-all` locally before pushing.
3. **Update `CHANGELOG.md`** under the `[Unreleased]` section if the change
   is user-visible.
4. **Open the PR** — keep it focused (one logical change per PR).
5. CI will run on your PR — please make sure it passes.

## Reporting bugs

When opening a bug report, please include:

- What you expected to happen
- What actually happened
- Steps to reproduce (a minimal code snippet helps a lot)
- Python version (`python --version`)
- `open-meteo-client` version (`python -c "import openmeteo; print(openmeteo.__version__)"`)

## Code of conduct

Be kind. This is a hobby project and I want it to stay fun. If you wouldn't
say it to a colleague's face, don't say it here.

## Questions

Not sure where to start? Open a [Discussion](https://github.com/jakobheine/open-meteo-client/discussions)
and tag it as a question.
