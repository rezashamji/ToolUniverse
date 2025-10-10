# Configuration file for Sphinx documentation with Shibuya theme.
# Modern, elegant theme with excellent sidebar navigation and i18n support

import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------
project = "ToolUniverse"
copyright = "2025, Shanghua Gao"
author = "Shanghua Gao"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
    "sphinx_design",
    "notfound.extension",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output with Shibuya theme -----------------------------
html_theme = "shibuya"
html_static_path = ["_static"]

# -- Shibuya theme configuration --------------------------------------------
html_theme_options = {
    # Navigation
    "nav_links": [
        {
            "title": "🏠 Home",
            "url": "index",
        },
        {
            "title": "📖 User Guide",
            "url": "guide/index",
        },
        {
            "title": "🔧 Tools",
            "url": "tools/tools_config_index",
        },
        {
            "title": "🎯 Tutorials",
            "url": "tutorials/index",
        },
    ],
    
    # GitHub integration
    "github_url": "https://github.com/mims-harvard/ToolUniverse",
    
    # Dark mode
    "dark_mode": True,
    
    # Colors (light mode)
    "light_logo": "_static/logo.png",
    "dark_logo": "_static/logo.png",
    
    # Accent color
    "accent_color": "blue",
    
    # Sidebar
    "globaltoc_expand_depth": 2,
    
    # Footer
    "twitter_site": False,
    "twitter_creator": False,
    "twitter_url": False,
    "discord_url": False,
    
    # Page layout
    "page_layout": "default",
    
    # Carbon ads (disabled)
    "carbon_ads_code": None,
    
    # Analytics (disabled)
    "analytics": {
        "google_analytics_id": "",
    },
}

# HTML options
html_title = f"{project} Documentation"
html_short_title = project
html_logo = "_static/logo.png" if os.path.exists("_static/logo.png") else None
html_favicon = "_static/logo_transparent.png" if os.path.exists("_static/logo_transparent.png") else None

# Custom CSS
html_css_files = [
    "custom.css",
]

# -- Autodoc configuration ---------------------------------------------------
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
}

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_class_signature = "separated"
autodoc_member_order = "bysource"

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

# MyST Parser settings
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "deflist",
    "html_admonition",
    "html_image",
    "colon_fence",
    "attrs_inline",
    "attrs_block",
    "linkify",
]

# Todo extension settings
todo_include_todos = True

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "requests": ("https://docs.python-requests.org/en/latest/", None),
}

# Sphinx-copybutton settings
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# Autosummary settings
autosummary_generate = True
autosummary_imported_members = True

# Source file suffixes
source_suffix = {
    ".rst": None,
    ".md": None,
}

# Master document
master_doc = "index"

# HTML options
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True

# Language and search
language = "en"
html_search_language = "en"

# Syntax highlighting
pygments_style = "default"
pygments_dark_style = "monokai"

# -- Internationalization (i18n) support -------------------------------------
locale_dirs = ["locale/"]
gettext_compact = False
gettext_uuid = True
gettext_location = True
gettext_auto_build = True

# Supported languages for version switcher
languages = {
    "en": "English",
    "zh_CN": "简体中文",
}

# -- Enhanced setup function -------------------------------------------------
def setup(app):
    """Custom Sphinx setup function."""
    app.add_css_file("custom.css")
    
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
