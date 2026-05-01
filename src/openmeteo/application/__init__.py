"""Application layer — use cases and orchestration.

Coordinates the domain with infrastructure to fulfill user intents. The
`Client` class (low-level) and the `weather` module (high-level helpers)
live here. Depends on domain and infrastructure; is depended on by the
package's public `__init__`.
"""
