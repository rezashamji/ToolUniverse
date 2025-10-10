# Configuration file for the Sphinx documentation builder with PyData theme.
# Modern, scientific-focused theme configuration for ToolUniverse

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
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
    "sphinx_design",
    "notfound.extension",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output with PyData theme ------------------------------
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

# -- PyData theme configuration ----------------------------------------------
html_theme_options = {
    # Branding
    "logo": {
        "text": "ToolUniverse",
        "image_light": "_static/logo.png",
        "image_dark": "_static/logo.png",
    },
    # Navigation
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "navbar_persistent": ["search-button"],
    # Footer
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version"],
    # GitHub integration
    "github_url": "https://github.com/mims-harvard/ToolUniverse",
    "use_edit_page_button": True,
    # Search
    "search_bar_text": "Search ToolUniverse docs...",
    "search_bar_position": "navbar",
    # External links
    "external_links": [
        {
            "name": "🧬 Bioinformatics",
            "url": "https://zitniklab.hms.harvard.edu/",
        },
        {
            "name": "📖 Tutorials",
            "url": "tutorials/index.html",
        },
    ],
    # Icon links
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/mims-harvard/ToolUniverse",
            "icon": "fab fa-github-square",
            "type": "fontawesome",
        },
        {
            "name": "Documentation",
            "url": "https://zitniklab.hms.harvard.edu/ToolUniverse/",
            "icon": "fas fa-book",
            "type": "fontawesome",
        },
    ],
    # Appearance
    "show_nav_level": 2,
    "show_toc_level": 2,
    "collapse_navigation": False,
    "navigation_depth": 4,
    # Theme options
    "show_prev_next": True,
    "show_version_warning_banner": True,
    # Sidebar
    "primary_sidebar_end": ["sidebar-ethical-ads"],
    "secondary_sidebar_items": ["page-toc", "edit-this-page"],
    # Analytics
    "analytics": {
        "google_analytics_id": "",  # Add if needed
    },
    # Custom CSS
    "pygments_light_style": "default",
    "pygments_dark_style": "monokai",
}

# Source repository configuration for edit buttons
html_context = {
    "github_user": "zitniklab",
    "github_repo": "ToolUniverse",
    "github_version": "main",
    "doc_path": "docs",
}

# -- Logo and branding -------------------------------------------------------
html_title = f"{project} Documentation"
html_logo = "_static/logo.png" if os.path.exists("_static/logo.png") else None
html_favicon = "_static/logo_transparent.png" if os.path.exists("_static/logo_transparent.png") else None

# -- Custom CSS for enhanced styling ----------------------------------------
html_css_files = [
    "pydata_custom.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
]

# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": "__init__",
}

# MyST parser settings
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "dollarmath",
    "amsmath",
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
copybutton_line_continuation_character = "\\"
copybutton_here_doc_delimiter = "EOF"

# Sphinx-tabs settings
sphinx_tabs_valid_builders = ["linkcheck"]
sphinx_tabs_disable_tab_closing = False

# NotFound extension settings
notfound_context = {
    "title": "Page Not Found",
    "body": """
    <div class="alert alert-warning" role="alert">
        <h4 class="alert-heading">🔍 Page Not Found</h4>
        <p>The page you're looking for doesn't exist. Here are some helpful links:</p>
        <hr>
        <div class="row">
            <div class="col-md-6">
                <h6>🏠 <a href="index.html">Home</a></h6>
                <h6>🚀 <a href="quickstart.html">Quick Start</a></h6>
                <h6>📖 <a href="guide/index.html">User Guide</a></h6>
            </div>
            <div class="col-md-6">
                <h6>🎯 <a href="tutorials/index.html">Tutorials</a></h6>
                <h6>📚 <a href="reference/index.html">Reference</a></h6>
                <h6>❓ <a href="help/faq.html">FAQ</a></h6>
            </div>
        </div>
    </div>
    """,
}

# Source file suffixes
source_suffix = {
    ".rst": None,
    ".md": None,
}

# Master document
master_doc = "index"

# GitHub Pages configuration
html_baseurl = "https://zitniklab.hms.harvard.edu/ToolUniverse/"
html_extra_path = []

# Enhanced HTML options for modern look
html_use_smartypants = False
html_show_sourcelink = True
html_show_sphinx = False
html_copy_source = False
html_show_copyright = True

# Language and search
language = "en"
html_search_language = "en"

# Modern meta tags for better SEO and social sharing
html_meta = {
    "description": "ToolUniverse: A comprehensive scientific AI tool collection for drug discovery, literature analysis, and research workflows.",
    "keywords": "AI tools, scientific research, drug discovery, bioinformatics, API integration",
    "author": "Shanghua Gao",
    "viewport": "width=device-width, initial-scale=1.0",
    "og:title": "ToolUniverse Documentation",
    "og:description": "Comprehensive scientific AI tool collection for researchers and developers.",
    "og:type": "website",
    "twitter:card": "summary_large_image",
}

# LaTeX configuration for PDF output
latex_elements = {
    "papersize": "letterpaper",
    "pointsize": "11pt",
    "fncychap": "\\usepackage[Bjornstrup]{fncychap}",
    "preamble": r"""
\usepackage{graphicx}
\usepackage{xcolor}
\definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
\definecolor{VerbatimBorderColor}{rgb}{0.8,0.8,0.8}
""",
}


# Custom setup function for additional enhancements
def setup(app):
    """Custom Sphinx setup function for enhanced functionality."""
    # Add custom CSS
    app.add_css_file("pydata_custom.css")

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
