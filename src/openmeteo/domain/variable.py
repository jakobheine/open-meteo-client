"""Weather variables (temperature_2m, precipitation, etc.).

The `Variable` enum is auto-generated from Open-Meteo's OpenAPI spec
(see `src/openmeteo/_generated/variables.py` and `scripts/regen_variables.py`).
We re-export it here so consumers can use the domain name and so we have
a place to add hand-written additions later if needed.
"""

from openmeteo._generated.variables import Variable

__all__ = ["Variable"]
