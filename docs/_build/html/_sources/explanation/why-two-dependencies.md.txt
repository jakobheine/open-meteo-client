# Why only two runtime dependencies

`open-meteo-client` has exactly two runtime dependencies:
[`httpx`](https://www.python-httpx.org/) and
[`pydantic`](https://docs.pydantic.dev/).

It doesn't use:

- `requests` — `httpx` supersedes it for new code (async support,
  HTTP/2, connection pooling semantics).
- `aiohttp` — `httpx` covers the same ground with a cleaner API.
- `flatbuffers` — Open-Meteo offers a FlatBuffers wire format, but JSON
  is fine for our scale and dramatically simpler to debug.
- `pandas` / `numpy` — would dwarf the library's own footprint, and the
  audience for `today("Dresden")` doesn't need a DataFrame.

## The shape of "lightweight"

| Dimension | Target |
|-----------|--------|
| Install size | under 20 MB including transitive deps |
| Import time | under 100 ms cold |
| Deps to pin in your `requirements.txt` | 2 |
| Security surface | as small as practical |

## Where this matters

- **AWS Lambda / serverless** — every MB and every ms of cold start counts.
- **Home automation (Home Assistant, openHAB)** — run on SBCs with
  modest memory.
- **CLI tools** — import time directly hits UX.

## Where it doesn't

- Data-science notebooks where you already have pandas loaded.
- Long-running services where import time is a one-time cost.

We're optimizing for the first group.
