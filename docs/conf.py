"""Sphinx configuration for open-meteo-client docs.

Docs: https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from __future__ import annotations

from importlib.metadata import version as _pkg_version

# -- Project information ------------------------------------------------------

project = "open-meteo-client"
author = "Jakob Heine"
copyright = f"2026, {author}"  # Sphinx expects this exact name

# Single source of truth — read from installed package metadata so docs
# and PyPI can never drift.
release = _pkg_version("open-meteo-client")
version = ".".join(release.split(".")[:2])

# -- General configuration ----------------------------------------------------

extensions = [
    # Core Sphinx extensions
    "sphinx.ext.autodoc",  # Pull docstrings into reference
    "sphinx.ext.napoleon",  # Parse Google-style docstrings
    "sphinx.ext.intersphinx",  # Cross-link to Python / httpx / pydantic docs
    "sphinx.ext.viewcode",  # "View source" links next to each entry
    # Third-party
    "myst_parser",  # Markdown support (we use .md for prose)
    "sphinx_autodoc_typehints",  # Render type hints nicely in signatures
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# MyST-parser — enable useful Markdown features
myst_enable_extensions = [
    "colon_fence",  # ::: admonition blocks
    "deflist",
    "smartquotes",
    "substitution",
    "tasklist",
]
myst_heading_anchors = 3  # auto-generate anchors for h1-h3

# -- Autodoc options ----------------------------------------------------------

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "member-order": "bysource",
}
autodoc_typehints = "description"  # put type hints in param/return sections
autodoc_typehints_description_target = "documented"
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_use_rtype = True

# -- Intersphinx --------------------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# -- HTML output --------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_title = f"{project} {release}"
html_show_sourcelink = True
html_last_updated_fmt = "%Y-%m-%d"

# RTD theme knobs
html_theme_options = {
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 3,
    "includehidden": True,
}
