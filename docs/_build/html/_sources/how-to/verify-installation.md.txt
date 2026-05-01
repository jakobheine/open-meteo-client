# Verify `open-meteo-client` is installed

You want to confirm `open-meteo-client` is installed and importable,
for example after provisioning a new environment or debugging a build.

## Solution

```python
from openmeteo import ping

print(ping())
```

Expected output:

```text
open-meteo-client 0.0.4: pong
```

- If you see `ModuleNotFoundError`, the package isn't installed in the
  active interpreter. Check with `python -m pip show open-meteo-client`.
- If you see a different version string, you have an older or newer
  release than expected.

`ping()` never raises, makes no network calls, and always returns a
string. It's safe to use in CI and startup checks.
