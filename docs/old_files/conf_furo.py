# Configuration file for the Sphinx documentation builder with Furo theme.
# Modern, clean, and responsive documentation theme configuration

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

# -- Options for HTML output with Furo theme --------------------------------
html_theme = "furo"
html_static_path = ["_static"]

# -- Enhanced Furo theme configuration ---------------------------------------
html_theme_options = {
    # Color scheme
    "light_css_variables": {
        "color-brand-primary": "#2980B9",
        "color-brand-content": "#2980B9",
        "color-admonition-background": "#f8f9fa",
        "color-api-background": "#f8f9fa",
        "color-api-background-hover": "#e9ecef",
        "color-sidebar-background": "#ffffff",
        "color-sidebar-background-border": "#eeeeee",
        # Typography
        "font-stack": "system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji",
        "font-stack--monospace": "Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace",
        # Spacing and sizes
        "sidebar-caption-space-above": "2rem",
        "api-font-size": "var(--font-size--small)",
        "admonition-font-size": "0.9rem",
        # Links
        "color-link": "#2980B9",
        "color-link--hover": "#1f5f8b",
    },
    "dark_css_variables": {
        "color-brand-primary": "#3498DB",
        "color-brand-content": "#3498DB",
        "color-admonition-background": "#1e1e1e",
        "color-api-background": "#1e1e1e",
        "color-api-background-hover": "#2d2d2d",
        "color-sidebar-background": "#131416",
        "color-sidebar-background-border": "#303335",
        # Dark mode typography
        "color-foreground-primary": "#efefef",
        "color-foreground-secondary": "#c9c9c9",
        "color-foreground-muted": "#81868d",
        # Dark mode links
        "color-link": "#3498DB",
        "color-link--hover": "#5dade2",
    },
    # Navigation and layout
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_button": None,
    # Code and content
    "source_repository": "https://github.com/mims-harvard/ToolUniverse",
    "source_branch": "main",
    "source_directory": "docs/",
    # Footer
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/mims-harvard/ToolUniverse",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "Slack",
            "url": "https://aiscientist.tools/#:~:text=Join%20Slack%20Community",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path d="M3.362 10.11c0 .926-.756 1.682-1.681 1.682S0 11.036 0 10.111C0 9.186.756 8.43 1.681 8.43h1.681v1.68zm.846 0c0-.924.756-1.68 1.681-1.68s1.681.756 1.681 1.68v4.21c0 .924-.756 1.68-1.681 1.68s-1.681-.756-1.681-1.68v-4.21zm6.725 1.682c-.926 0-1.682-.756-1.682-1.681s.756-1.681 1.682-1.681h1.681v1.681c0 .925-.756 1.681-1.681 1.681zm-1.681-1.682c0-.924.756-1.68 1.681-1.68s1.681.756 1.681 1.68v1.681H9.431v-1.68zm1.681-6.725c.926 0 1.681-.756 1.681-1.681S11.037 0 10.112 0H8.43v1.681c0 .926.756 1.681 1.681 1.681zm-1.681 0c0 .924-.756 1.68-1.681 1.68S5.069 2.405 5.069 1.48V0H3.388v1.48c0 .924.756 1.68 1.681 1.68zm1.681 0c.926 0 1.681.756 1.681 1.681s-.756 1.681-1.681 1.681H8.43V1.681c0-.925.756-1.681 1.681-1.681zM5.069 1.681c0-.925.756-1.681 1.681-1.681s1.681.756 1.681 1.681v1.681H5.069V1.681zm-1.681 6.725c-.926 0-1.681.756-1.681 1.681s.756 1.681 1.681 1.681h1.681V9.431c0-.925-.756-1.681-1.681-1.681zm0 .846c.924 0 1.68.756 1.68 1.681s-.756 1.681-1.68 1.681H1.681c-.925 0-1.681-.756-1.681-1.681s.756-1.681 1.681-1.681h1.681zm6.725-1.681c0 .926-.756 1.682-1.681 1.682s-1.681-.756-1.681-1.682V5.069h1.681c.925 0 1.681.756 1.681 1.681z"/>
                </svg>
            """,
            "class": "",
        },
    ],
}

# -- Logo and branding -------------------------------------------------------
html_title = f"{project} Documentation"
html_logo = "_static/logo.png" if os.path.exists("_static/logo.png") else None
html_favicon = "_static/logo_transparent.png" if os.path.exists("_static/logo_transparent.png") else None

# -- Custom CSS for enhanced styling ----------------------------------------
html_css_files = [
    "furo_custom.css",
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
    <h2>🔍 Oops! Page not found.</h2>
    <p>The page you're looking for doesn't exist. Here are some helpful links:</p>
    <div class="admonition tip">
        <p class="admonition-title">Quick Navigation</p>
        <ul>
            <li><a href="index.html">🏠 Home</a></li>
            <li><a href="quickstart.html">🚀 Quick Start</a></li>
            <li><a href="guide/index.html">📖 User Guide</a></li>
            <li><a href="help/faq.html">❓ FAQ</a></li>
        </ul>
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
html_show_sphinx = False  # Hide "Made with Sphinx" for cleaner footer
html_copy_source = False
html_show_copyright = True

# Language and search
language = "en"
html_search_language = "en"

# Better source code highlighting
pygments_style = "default"
pygments_dark_style = "monokai"  # Dark mode syntax highlighting

# Enhanced navigation
html_use_index = True
html_split_index = False
html_domain_indices = True

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


# Custom setup function for additional enhancements
def setup(app):
    """Custom Sphinx setup function for enhanced functionality."""
    # Add custom CSS
    app.add_css_file("furo_custom.css")

    # Add analytics if needed
    # app.add_js_file('analytics.js')

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
