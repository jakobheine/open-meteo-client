# Architecture

`open-meteo-client` uses lightweight Domain-Driven Design layering to
keep concerns separable without over-engineering.

## Layers

```
src/openmeteo/
├── domain/            pure domain types (Location, Forecast, Variable, UnitSystem)
├── application/       orchestration (Client, weather helpers, ping)
├── infrastructure/    external IO (httpx adapter, geocoding, response parsing)
└── _generated/        code generated from Open-Meteo's OpenAPI spec
```

Dependencies flow **inward only**:

- `domain/` imports nothing from this package.
- `application/` imports from `domain/` and `infrastructure/`.
- `infrastructure/` imports from `domain/` only.
- The package root (`openmeteo/__init__.py`) re-exports the public API
  from `application/`.

## Why this structure

For a small library this is arguably heavier than strictly necessary —
most async HTTP clients are one or two modules. We adopt it anyway for
three reasons:

1. **Testability.** The `domain/` layer is pure, so unit tests run in
   microseconds and need no mocking.
2. **Swappability.** `infrastructure/` is isolated behind interfaces
   that `application/` consumes. Moving from `httpx` to some other
   transport would touch a bounded set of files.
3. **Readability.** File names tell you what each thing is.
   `domain/variable.py` ≠ `infrastructure/http.py` at a glance.

## Anti-goals

- We do *not* ship a "hexagonal ports and adapters" framework. The
  "layers" are just module boundaries enforced by code review, not by
  a registry or a DI container.
- We do *not* split into multiple packages. A library this size doesn't
  need a monorepo.
- We do *not* expose the layers as a stable public contract. The only
  thing guaranteed stable is what's re-exported from `openmeteo` itself.

## Code generation

[`src/openmeteo/_generated/variables.py`](https://github.com/jakobheine/open-meteo-client/blob/main/src/openmeteo/_generated/variables.py)
holds the `Variable` enum, auto-regenerated from Open-Meteo's OpenAPI
spec via `just regen-variables`. CI verifies the committed file matches
what re-running the script would produce; manual edits to generated
files fail the build.
