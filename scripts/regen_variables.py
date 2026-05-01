"""Regenerate `src/openmeteo/_generated/variables.py` from Open-Meteo's OpenAPI spec.

Fetches the upstream OpenAPI YAML, extracts the weather variable enums
from the `/v1/forecast` endpoint's `hourly`, `daily`, and `current`
parameters, and writes a `StrEnum` to the _generated module.

Run via `just regen-variables`. CI verifies the committed file matches
what re-running this script would produce.

Idempotency: running twice in a row produces byte-identical output
(sorted, formatted via `ruff format`).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import httpx
import yaml

OPENAPI_URL = "https://raw.githubusercontent.com/open-meteo/open-meteo/main/openapi.yml"
TARGET = (
    Path(__file__).resolve().parent.parent / "src" / "openmeteo" / "_generated" / "variables.py"
)
FORECAST_PATH = "/v1/forecast"
PARAMETER_NAMES = ("hourly", "daily", "current")


def fetch_spec(url: str) -> dict[str, Any]:
    """Download and parse the Open-Meteo OpenAPI spec."""
    print(f"Fetching {url}")
    response = httpx.get(url, timeout=30.0, follow_redirects=True)
    response.raise_for_status()
    parsed: dict[str, Any] = yaml.safe_load(response.text)
    return parsed


def extract_enum_values(spec: dict[str, Any]) -> dict[str, list[str]]:
    """Pull variable enums from the forecast endpoint's parameters.

    Returns a dict mapping parameter name (hourly/daily/current) to its
    sorted, deduplicated list of valid values.
    """
    path_item = spec["paths"][FORECAST_PATH]
    get_op = path_item["get"]
    parameters = get_op["parameters"]

    enums: dict[str, list[str]] = {}
    for param in parameters:
        name = param.get("name")
        if name not in PARAMETER_NAMES:
            continue
        schema = param.get("schema", {})
        items = schema.get("items", {})
        values = items.get("enum")
        if not values:
            continue
        enums[name] = sorted(set(values))

    for p in PARAMETER_NAMES:
        if p not in enums:
            print(f"WARNING: parameter '{p}' not found in OpenAPI spec", file=sys.stderr)

    return enums


def variable_name_to_python(value: str) -> str:
    """Turn an API variable name like 'temperature_2m' into an enum member name.

    Rules:
    - Uppercase
    - Ensure it's a valid Python identifier (starts with a letter or _)
    - Leading digits get an underscore prefix
    """
    upper = value.upper()
    if upper and upper[0].isdigit():
        upper = f"_{upper}"
    return upper


def render(enums: dict[str, list[str]]) -> str:
    """Render the _generated/variables.py source."""
    # Merge all values from all parameter groups; a value may appear in
    # more than one (e.g. `temperature_2m` in hourly, `temperature_2m_max`
    # only in daily). We keep them all in one Variable enum for simplicity.
    all_values: set[str] = set()
    for values in enums.values():
        all_values.update(values)
    sorted_values = sorted(all_values)

    lines: list[str] = [
        '"""Variable enum auto-generated from Open-Meteo OpenAPI spec.',
        "",
        "DO NOT EDIT. Regenerate via `just regen-variables`.",
        f"Source: {OPENAPI_URL}",
        '"""',
        "",
        "from enum import StrEnum",
        "",
        "",
        "class Variable(StrEnum):",
        '    """Weather variable names accepted by the Open-Meteo forecast API."""',
        "",
    ]
    lines.extend(f"    {variable_name_to_python(value)} = {value!r}" for value in sorted_values)
    lines.append("")  # trailing newline
    return "\n".join(lines)


def format_with_ruff(path: Path) -> None:
    """Run `ruff format` on the generated file so it matches repo style."""
    subprocess.run(["ruff", "format", str(path)], check=True)  # noqa: S603, S607


def main() -> int:
    """Fetch the OpenAPI spec, extract variables, write the _generated file."""
    spec = fetch_spec(OPENAPI_URL)
    enums = extract_enum_values(spec)
    total = sum(len(v) for v in enums.values())
    print(f"Extracted {total} variable values across {', '.join(enums)}")

    content = render(enums)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(content, encoding="utf-8")
    print(f"Wrote {TARGET.relative_to(Path.cwd())}")

    format_with_ruff(TARGET)
    print("Formatted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
