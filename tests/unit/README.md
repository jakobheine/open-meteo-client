# Unit tests

Pure unit tests of individual modules. No IO, no mocks of external
services, no network.

**What belongs here:**
- Domain logic (value objects, enums, pure functions)
- Package metadata (version, imports)
- Utility / helper functions

**What does NOT belong here:**
- Tests that mock `httpx` — those go in `../integration/`
- Tests that hit the real API — those go in `../live/`
