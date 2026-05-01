# Live tests

Tests that hit the **real Open-Meteo API**. Run by a scheduled GitHub
workflow (daily) and on demand before releases; excluded from the
default `just test` / `just check` runs.

Every test here must be marked `@pytest.mark.live`.

**What belongs here:**
- Smoke checks against real endpoints ("does the API still accept our
  request shape?")
- Canaries for API drift detection

**Guidelines:**
- Assert ranges, not exact values (`-50 < temperature < 60`, never
  `temperature == 14.2`)
- Retry-tolerant: a single network hiccup shouldn't fail the suite
  (configure `pytest-rerunfailures`)
- Minimal payloads: don't spam Open-Meteo; one forecast per test is plenty

See issue #8 for the scheduled workflow plan.
