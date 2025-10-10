# Enhanced Configuration file for the Sphinx documentation builder.
# This file provides comprehensive docstring extraction and documentation generation

import os
import sys
from pathlib import Path

# Add source directory to Python path
sys.path.insert(0, os.path.abspath("../src"))

# Project information
project = "ToolUniverse"
copyright = "2025, Shanghua Gao"
author = "Shanghua Gao"
release = "1.0.0"
version = "1.0.0"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    "myst_parser",
    "sphinx_rtd_theme",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
]

# Template paths and exclusions
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "venv", "__pycache__"]

# HTML output configuration
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Enhanced Napoleon settings for better docstring parsing
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = [
    ("Returns", "params_style"),
    ("Yields", "params_style"),
    ("Examples", "examples_style"),
    ("Usage", "examples_style"),
    ("Configuration", "params_style"),
]

# Enhanced Autodoc settings for comprehensive docstring extraction
autodoc_default_options = {
    "members": True,
    "member-order": "alphabetical",
    "special-members": "__init__,__call__,__getitem__,__setitem__",
    "undoc-members": True,
    "exclude-members": "__weakref__,__dict__,__module__",
    "show-inheritance": True,
    "private-members": True,
    "inherited-members": True,
}

# Advanced autodoc configuration
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_typehints_format = "short"
autoclass_content = "both"  # Include both class and __init__ docstrings
autodoc_preserve_defaults = True
autodoc_member_order = "alphabetical"

# Mock imports for external dependencies that might not be available
autodoc_mock_imports = [
    "numpy",
    "pandas",
    "requests",
    "matplotlib",
    "seaborn",
    "plotly",
    "networkx",
    "scipy",
    "sklearn",
    "transformers",
    "torch",
    "tensorflow",
    "openai",
    "anthropic",
    "django",
    "flask",
    "fastapi",
    "pydantic",
    "sqlalchemy",
    "celery",
    "redis",
    "pymongo",
    "psycopg2",
    "mysql",
    "boto3",
    "azure",
    "gcp",
    "streamlit",
    "gradio",
    "jupyterlab",
]

# Autosummary settings for automatic API documentation
autosummary_generate = True
autosummary_generate_overwrite = True
autosummary_imported_members = True

# MyST parser settings for Markdown support
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "dollarmath",
    "amsmath",
    "colon_fence",
    "attrs_inline",
    "attrs_block",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
]

# Advanced HTML theme options
html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "vcs_pageview_mode": "blob",
    "style_nav_header_background": "#2980B9",
    # Toc options
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 5,
    "includehidden": True,
    "titles_only": False,
    # Additional options
    "canonical_url": "",
    "analytics_id": "",
    "analytics_anonymize_ip": False,
}

# Additional HTML configuration
html_logo = "_static/logo.png" if os.path.exists("_static/logo.png") else None
html_favicon = "_static/logo_transparent.png" if os.path.exists("_static/logo_transparent.png") else None
html_title = f"{project} Documentation"
html_short_title = project
html_last_updated_fmt = "%b %d, %Y"
html_use_smartypants = True
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

# Custom CSS
html_css_files = [
    "custom.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
]

# Custom JavaScript
html_js_files = [
    "custom.js",
]

# Source file suffixes
source_suffix = {
    ".rst": None,
    ".md": None,
    ".txt": None,
}

# Master document
master_doc = "index"

# Todo extension settings
todo_include_todos = True
todo_emit_warnings = True

# Intersphinx mapping for external documentation
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "requests": ("https://docs.python-requests.org/en/latest/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "networkx": ("https://networkx.org/documentation/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
}

# GitHub Pages configuration
html_baseurl = "https://zitniklab.hms.harvard.edu/ToolUniverse/"
html_extra_path = []

# Copy button configuration
copybutton_prompt_text = "$ "
copybutton_prompt_is_regexp = True
copybutton_line_continuation_character = "\\"

# Inheritance diagram configuration
inheritance_graph_attrs = dict(
    rankdir="TB", size='"6.0, 8.0"', fontsize=14, ratio="compress"
)
inheritance_node_attrs = dict(
    shape="ellipse", fontsize=14, color="blue", style="filled", fillcolor="lightblue"
)
inheritance_edge_attrs = dict(penwidth=0.75)

# Coverage extension configuration
coverage_show_missing_items = True
coverage_ignore_modules = [
    "tests",
    "test_*",
    "conftest",
    "setup",
]

# Graphviz configuration
graphviz_output_format = "svg"


# Custom roles and directives
def setup(app):
    """Custom Sphinx setup function."""

    # Add custom CSS
    app.add_css_file("custom.css")

    # Add custom directive for function examples
    try:
        from docutils import nodes
        from docutils.parsers.rst import Directive

        class ExampleDirective(Directive):
            """Custom directive for function usage examples."""

            has_content = True
            required_arguments = 0
            optional_arguments = 1

            def run(self):
                content = "\n".join(self.content)
                example_node = nodes.literal_block(content, content)
                example_node["language"] = "python"
                example_node["classes"] = ["example-code"]

                container = nodes.container()
                container["classes"] = ["example-container"]

                title = nodes.title("Example", "Example")
                title["classes"] = ["example-title"]

                container += title
                container += example_node

                return [container]

        app.add_directive("example", ExampleDirective)
    except ImportError:
        # If docutils is not available, skip custom directive
        pass

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


# Suppress specific warnings
suppress_warnings = [
    "myst.xref_missing",
    "toc.not_included",
]

# Additional configuration for better documentation generation
add_function_parentheses = True
add_module_names = True
python_use_unqualified_type_names = True

# Language and locale
language = "en"
locale_dirs = ["locale/"]
gettext_compact = False

# Figure numbering
numfig = True
numfig_format = {
    "figure": "Figure %s",
    "table": "Table %s",
    "code-block": "Listing %s",
    "section": "Section %s",
}

# LaTeX configuration for PDF output
latex_elements = {
    "papersize": "letterpaper",
    "pointsize": "10pt",
    "preamble": r"""
\usepackage{graphicx}
\usepackage{xcolor}
\definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
\definecolor{VerbatimBorderColor}{rgb}{0.8,0.8,0.8}
""",
    "fncychap": "\\usepackage[Bjornstrup]{fncychap}",
    "printindex": "\\footnotesize\\raggedright\\printindex",
}

latex_documents = [
    (
        master_doc,
        "ToolUniverse.tex",
        "ToolUniverse Documentation",
        "Shanghua Gao",
        "manual",
    ),
]

# Manual page output
man_pages = [(master_doc, "tooluniverse", "ToolUniverse Documentation", [author], 1)]

# Texinfo output
texinfo_documents = [
    (
        master_doc,
        "ToolUniverse",
        "ToolUniverse Documentation",
        author,
        "ToolUniverse",
        "A comprehensive scientific AI tool collection.",
        "Miscellaneous",
    ),
]

# EPUB output
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ["search.html"]
