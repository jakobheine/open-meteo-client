---
id: docs-freshness
description: >
  Keep README, Sphinx docs, CHANGELOG, and project-metadata in sync with
  the code. Invoked before every commit that touches production code or
  user-visible behavior. Never touches auto-generated files.
trigger: pre-commit (manual, via `just docs-check` or by asking the agent)
applies_to:
  - src/**
  - pyproject.toml
  - .github/workflows/**
  - justfile
  - CHANGELOG.md
  - README.md
  - docs/**
never_modify:
  - src/openmeteo/_generated/**   # regenerated via `just regen-variables`
  - docs/_build/**                # Sphinx build output
  - uv.lock                        # reviewed, not edited directly
  - tests/fixtures/**              # captured real responses
inputs:
  - base: git ref (default: last commit on origin/main)
  - head: git ref (default: working tree)
outputs:
  - report: bullet list of findings
  - patches: proposed file edits, offered for human approval before apply
version: 1
---

# SOP: docs-freshness

## Purpose

Whenever the codebase changes in a way a user might notice, the docs
should reflect it. Running this SOP before every commit keeps
documentation from silently rotting behind the code.

## When to run

**You MUST run this SOP before proposing a commit that touches any of
the files listed under `applies_to` above.**

You MAY skip this SOP when:

- The diff is *only* inside `tests/**`
- The diff is *only* inside `docs/**` (the docs themselves are the
  subject of the change; recursive check not needed)
- The commit is purely a release version bump (e.g., changing
  `__version__` and the `CHANGELOG.md` heading — the user explicitly
  already did the docs work)

When in doubt, run it.

## Procedure

### Step 1 — Establish the diff

1. If the user didn't specify `base`, use `origin/main` as the baseline.
2. Collect all file changes between `base` and the working tree.
3. Classify each changed file into one of:
   - `code` — `src/openmeteo/**`, excluding `_generated/**`
   - `public-surface` — `src/openmeteo/__init__.py` (public re-exports)
   - `metadata` — `pyproject.toml`, `AGENTS.md`, `CONTRIBUTING.md`, badges in `README.md`
   - `tooling` — `justfile`, `.github/workflows/**`, `.readthedocs.yaml`,
     `.codecov.yml`, `.coderabbit.yaml`, `.pre-commit-config.yaml`
   - `docs` — `docs/**` (excluding `_build/`)
   - `changelog` — `CHANGELOG.md`
   - `readme` — `README.md` (outside badges)
   - `never_modify` — anything in the list above
4. If anything in `never_modify` changed: **STOP. Output a report
   flagging the improper change and propose no patches.** The user
   must revert or regenerate those files via the proper mechanism
   (`just regen-variables`, etc.).

### Step 2 — Read the current documentation

Before proposing any changes, load the current state of:

- `README.md`
- `CHANGELOG.md` (at least the `[Unreleased]` section)
- `docs/index.md`
- Each file under `docs/tutorial/`, `docs/how-to/`, `docs/explanation/`

The reference section (`docs/reference/**`) is auto-generated from
docstrings; **you MUST NOT edit it here**. Instead, if the diff changes
a public docstring, note that the reference will regenerate on the
next RTD build — no manual action needed.

### Step 3 — Derive required doc updates

For each change, ask:

1. **Is this change user-visible?**
   - New/removed/renamed public function, class, parameter, or behavior
   - New dependency shown in `pyproject.toml`
   - Changed install flow, supported Python versions, or OS support
   - New CI job or release gate that contributors would hit
   - Answer yes → requires at least a `CHANGELOG.md` entry
2. **Does it change how a new user gets started?**
   - New preferred install instruction, first-call example, minimum
     version, etc.
   - Answer yes → requires a `README.md` update **and** a
     `docs/tutorial/getting-started.md` update
3. **Does it change a how-to recipe?**
   - Scan `docs/how-to/**`; if any existing guide's steps still read
     right, fine; if a step is now wrong, mark that guide for update
4. **Does it change the architecture or a documented decision?**
   - If yes → `docs/explanation/architecture.md` and/or relevant
     `docs/explanation/why-*.md`
5. **Does it add something docstring-worthy?**
   - New public function/class without a Google-style docstring: flag
     this as a **code** requirement (not a docs one). Do not write the
     docstring here; ask the user to add it in the source. The
     reference regen will pick it up.

### Step 4 — Check meta status

You MUST also verify:

- `pyproject.toml` `Development Status` classifier and README `Status`
  banner agree with each other.
- The implicit project phase is accurate. Use this rule:
  - **Planning (1)** — no production code that makes network calls
  - **Pre-Alpha (2)** — at least one real public function with real IO
    exists, but incomplete / likely to change
  - **Alpha (3)** — the documented v0.1.0 feature set works; API may
    change before v1
  - **Beta (4)** — feature-complete against the v1 goal; bugs expected
  - **Production (5)** — API committed; SemVer promises apply

If the phase needs changing, propose the update to both `pyproject.toml`
and `README.md` as a patch.

### Step 5 — Propose the report

Produce a single structured report with this shape:

```
# docs-freshness report

Files changed since {base}: N
Classified as: code=X, metadata=Y, ...

## Required updates
- [ ] CHANGELOG.md [Unreleased]: add "Added: `openmeteo.foo()` ..."
- [ ] README.md: update the example snippet to include `foo()`
- [ ] docs/tutorial/getting-started.md: mention `foo()` in the snippet
- (...)

## Optional updates
- Consider adding a how-to: "Using foo() with Home Assistant"

## Flagged issues
- (any never_modify violations, missing docstrings, phase mismatches)

## Proposed patches
- (inline diffs for each required update, ready to apply)
```

### Step 6 — Hand off for approval

**You MUST NOT apply the patches without explicit user approval.**

Present the report. Wait for the user to say "apply" or give targeted
instructions. After they approve:

1. Apply the patches exactly as proposed
2. Run `just check` to verify nothing regressed
3. Stage the doc changes alongside the original code changes
4. Propose a single commit that bundles both under a descriptive message
   (or separate commits if the user prefers — default to bundled)

## Non-goals

- **Auto-writing API reference prose.** That's Sphinx + docstrings.
- **Auto-editing auto-generated files.** See `never_modify`.
- **Speculating about future features.** Only document what's in the
  diff.
- **Being nice.** If the phase is wrong, say so. If a new function has
  no docstring, say so. Calibration beats flattery.

## Conventions

- Google-style docstrings for any new public surface
- Line length 100, same as the rest of the project (ruff-enforced)
- CHANGELOG entries under `[Unreleased]` follow Keep a Changelog
  categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`,
  `Security`

## Self-check

Before declaring "done":

- [ ] No edits in `never_modify` paths
- [ ] CHANGELOG updated if the change is user-visible
- [ ] README banner/badges match the current phase
- [ ] `just check` passes
- [ ] All proposed patches approved by the user before apply
