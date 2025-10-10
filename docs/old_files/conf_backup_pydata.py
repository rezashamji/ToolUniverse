# Configuration file for the Sphinx documentation builder with PyData theme.
# Modern, vibrant, and multilingual documentation theme configuration

import os
import sys
import re
import textwrap
import warnings

try:
    import pydata_sphinx_theme  # noqa: F401
    PYDATA_THEME_AVAILABLE = True  # PyData 主题支持语言切换和现代化设计
except ImportError:  # pragma: no cover - diagnostic path
    PYDATA_THEME_AVAILABLE = False
    warnings.warn(
        "pydata-sphinx-theme is not installed; falling back to the Furo theme.",
        RuntimeWarning,
    )

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
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.linkcode",
    "sphinx_autodoc_typehints",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
    "sphinx_design",
    "notfound.extension",
]

# -- Toctree configuration ---------------------------------------------------
# Include hidden toctree entries in the sidebar navigation
toc_includehidden = True

# Sphinx sidebar configuration
# Make sure the globaltoc shows all entries
html_sidebars_default_level = 0

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output with theme fallbacks ----------------------------
html_static_path = ["_static"]

if PYDATA_THEME_AVAILABLE:
    html_theme = "pydata_sphinx_theme"
    html_theme_options = {
        "logo": {
            "text": "ToolUniverse",
        },
        "navbar_start": ["navbar-logo"],
        "navbar_center": [],
        "navbar_end": [
            "theme-switcher",
            "navbar-icon-links",
        ],
        "header_links_before_dropdown": 4,
        "icon_links": [
            {
                "name": "GitHub",
                "url": "https://github.com/mims-harvard/ToolUniverse",
                "icon": "fa-brands fa-github",
                "type": "fontawesome",
            },
            {
                "name": "Slack",
                "url": "https://aiscientist.tools/#:~:text=Join%20Slack%20Community",
                "icon": "fa-brands fa-slack",
                "type": "fontawesome",
            },
        ],
        # 左侧边栏配置 - 显示完整的导航树
        "show_nav_level": 2,  # 展开显示2层导航
        "navigation_depth": 4,  # 允许最多4层导航深度
        "collapse_navigation": False,  # 不折叠导航,显示所有层级
        "show_toc_level": 3,  # 页面目录显示深度
        "sidebar_includehidden": True,  # 包含隐藏的toctree条目，防止侧边栏被隐藏
        # 右侧边栏配置
        "secondary_sidebar_items": ["page-toc"],  # 右侧侧边栏显示页面目录
        "navigation_with_keys": True,
        # 语言切换器配置 (如果需要多语言版本)
        # "switcher": {
        #     "json_url": "https://tooluniverse.readthedocs.io/_static/switcher.json",
        #     "version_match": "latest",
        # },
    }
    # 配置侧边栏显示完整的全局导航树
    # PyData theme uses its own default sidebar templates
    html_sidebars = {
        "**": ["sidebar-nav-bs.html"]  # 左侧显示完整的导航树
    }
    html_css_files = ["pydata_custom.css"]
else:
    html_theme = "furo"
    html_theme_options = {
        "light_logo": "logo.png",
        "dark_logo": "logo.png",
    }
    html_css_files = ["furo_custom.css"]

html_context = {
    "default_mode": "light",
    "languages": [
        ("English", "/en/"),
        ("简体中文", "/zh-CN/"),
    ],
}

# -- Logo and branding -------------------------------------------------------
html_title = f"{project} Documentation"
html_logo = "_static/logo.png" if os.path.exists("_static/logo.png") else None
html_favicon = "_static/logo_transparent.png" if os.path.exists("_static/logo_transparent.png") else None

# -- Custom CSS for enhanced styling ----------------------------------------

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

# Autodoc settings - Enhanced to include all functions and classes
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": "__init__,__call__,__str__,__repr__",
    "private-members": False,
    "exclude-members": "__weakref__",
    "member-order": "bysource",
    "imported-members": True,
    "show-source": True,
}

# Render type hints in the description for better readability
autodoc_typehints = "description"
typehints_defaults = "comma"
typehints_fully_qualified = False

# Avoid importing heavy optional dependencies during docs build
autodoc_mock_imports = [
    "torch",
    "torchvision",
    "torchaudio",
    "chemprop",
    "admet_ai",
    "chemfunc",
    "faiss",
    "faiss_cpu",
    "faiss-gpu",
    "playwright",
    "pygraphviz",
    "graphviz",
    "pydot",
    "matplotlib",
    "rdkit",
    "sklearn",
    "scipy",
    "sentence_transformers",
    "transformers",
    "safetensors",
    "safetensors.torch",
]

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

# Autosummary settings for comprehensive API documentation
autosummary_generate = True
autosummary_imported_members = True
autosummary_ignore_module_all = False

# Autosectionlabel settings
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 3

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
            <li><a href="help/index.html">❓ Help</a></li>
        </ul>
    </div>
    """,
}

# Source file suffixes
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
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

# -- Warning suppression -----------------------------------------------------
# Suppress warnings for external libraries (Flask, etc.)
suppress_warnings = [
    "ref.doc",  # Suppress unknown document warnings
    "ref.ref",  # Suppress undefined label warnings
]

# -- Intersphinx mapping for external libraries -----------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "flask": ("https://flask.palletsprojects.com/", None),
}

# -- Doctest configuration --------------------------------------------------
doctest_test_doctest_blocks = 'default'
doctest_global_setup = '''
import sys
import os
sys.path.insert(0, os.path.abspath('../src'))
'''
doctest_global_cleanup = '''
# Cleanup code if needed
'''

# -- Extlinks configuration --------------------------------------------------
extlinks = {
    'issue': ('https://github.com/mims-harvard/ToolUniverse/issues/%s', 'issue #%s'),
    'pr': ('https://github.com/mims-harvard/ToolUniverse/pull/%s', 'PR #%s'),
    'commit': ('https://github.com/mims-harvard/ToolUniverse/commit/%s', 'commit %s'),
    'github': ('https://github.com/mims-harvard/ToolUniverse/%s', '%s'),
}

# -- Linkcode configuration --------------------------------------------------


def linkcode_resolve(domain, info):
    """Resolve links to source code."""
    if domain != 'py':
        return None
    
    filename = info['module'].replace('.', '/')
    
    # Handle different module patterns
    if filename.startswith('tooluniverse/'):
        # Remove the tooluniverse/ prefix for GitHub links
        filename = filename[12:]  # Remove 'tooluniverse/'
        return (f"https://github.com/mims-harvard/ToolUniverse/blob/"
                f"main/src/tooluniverse/{filename}.py")
    else:
        return (f"https://github.com/mims-harvard/ToolUniverse/blob/"
                f"main/src/tooluniverse/{filename}.py")



# Custom setup function for additional enhancements


def setup(app):
    """Custom Sphinx setup function for enhanced functionality."""
    # Add custom CSS
    app.add_css_file("pydata_custom.css")

    def _apply_language_context(app, config):
        ctx = dict(config.html_context or {})
        ctx.setdefault(
            "languages",
            [
                ("English", "/en/"),
                ("简体中文", "/zh-CN/"),
            ],
        )
        ctx["language"] = config.language or ctx.get("language") or "en"
        config.html_context = ctx

    app.connect("config-inited", _apply_language_context)

    # Add analytics if needed
    # app.add_js_file('analytics.js')

    # Normalize Markdown-style constructs in docstrings to valid reStructuredText
    def _normalize_markdown_in_docstrings(app, what, name, obj, options, lines):
        text = "\n".join(lines)
        text = textwrap.dedent(text)

        # 1) Convert fenced code blocks ```lang ... ``` to RST code-blocks
        def repl_codeblock(match):
            lang = match.group(1) or ""
            code = match.group(2).rstrip()
            if lang:
                header = f".. code-block:: {lang}\n\n"
            else:
                header = "::\n\n"
            indented = "\n".join([f"    {ln}" if ln else "" for ln in code.split("\n")])
            return f"{header}{indented}\n\n"

        codeblock_re = re.compile(
            r"```([a-zA-Z0-9_+-]*)\n([\s\S]*?)\n```",
            re.DOTALL,
        )
        text = codeblock_re.sub(repl_codeblock, text)

        # 2) Convert inline code `x` to RST literals ``x`` (avoid triple/backtick blocks already handled)
        inline_code_re = re.compile(r"`([^`\n]+)`")
        text = inline_code_re.sub(r"``\1``", text)

        # 3) Ensure a blank line after block quotes and directives to avoid "unexpected unindent"
        # Add a blank line after lines ending with '::' if not followed by blank
        colon_re = re.compile(r"(::)\n(\S)")
        text = colon_re.sub(r"\1\n\n\2", text)

        # 4) Balance stray strong markers: replace lone '**' around single words with '**word**'
        # If there is an opening ** without closing before whitespace/newline, escape it
        stray_strong_re = re.compile(r"\*\*(?![^*]+\*\*)")
        text = stray_strong_re.sub(r"\\**", text)

        # 5) Normalize indentation in literal blocks (convert tabs to 4 spaces inside code blocks only)
        def untab_code_blocks(m):
            block = m.group(0)
            return block.replace("\t", "    ")

        untab_re = re.compile(
            r"(?:\n\s*\.\.\s?code-block::[\s\S]*?\n)"
            r"(?:[ ]{0,3}[^\S\n]*\S[\s\S]*?)(?=\n\S|\Z)",
            re.DOTALL,
        )
        text = untab_re.sub(untab_code_blocks, text)

        # 6) Fix section underline lengths like "Title" followed by =====
        def fix_underline(match):
            title = match.group(1)
            underline = match.group(2)
            char = underline.strip()[:1] if underline.strip() else "="
            fixed = char * len(title)
            return f"{title}\n{fixed}\n"

        heading_re = re.compile(r"(^[^\n].*?)\n([=\-~^`:\\+#\*]{2,})\n", re.MULTILINE)
        text = heading_re.sub(fix_underline, text)

        # 7) Ensure blank line before and after section headings
        text = re.sub(r"(\S.*\n[=\-~^`:\\+#\*]{2,}\n)(?!\n)", r"\1\n", text)
        text = re.sub(r"(?<!\n)(\n\S.*\n[=\-~^`:\\+#\*]{2,}\n)", r"\n\1", text)

        # Write back to lines
        lines[:] = text.split("\n")

    app.connect("autodoc-process-docstring", _normalize_markdown_in_docstrings)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
