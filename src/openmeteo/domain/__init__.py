"""Domain layer — pure domain types and logic.

No IO, no network, no framework dependencies. The domain layer describes
the weather domain in its own vocabulary: forecasts, locations, variables,
units. It is safe to import from anywhere; it imports from nowhere else in
this package.

Aggregates and value objects live here.
"""
