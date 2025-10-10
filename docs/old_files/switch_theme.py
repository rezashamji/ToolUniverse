#!/usr/bin/env python3
"""
ToolUniverse Documentation Theme Switcher

This script allows you to easily switch between different modern Sphinx themes
for the ToolUniverse documentation.

Available themes:
1. Furo - Modern, clean theme with dark/light mode support
2. PyData - Scientific documentation theme based on Bootstrap
3. RTD (Read the Docs) - Original theme with custom enhancements

Usage:
    python switch_theme.py furo
    python switch_theme.py pydata
    python switch_theme.py rtd
    python switch_theme.py --list
    python switch_theme.py --compare
"""

import argparse
import shutil
import os
import sys
from pathlib import Path

# Theme configurations
THEMES = {
    "furo": {
        "name": "Furo",
        "description": "Modern, clean theme with dark/light mode support",
        "config_file": "conf_furo.py",
        "requirements": ["furo"],
        "pros": [
            "✅ Most modern and clean design",
            "✅ Built-in dark/light mode toggle",
            "✅ Excellent mobile responsiveness",
            "✅ Fast loading and performance",
            "✅ Beautiful code highlighting",
            "✅ Accessible and keyboard navigation",
        ],
        "cons": [
            "⚠️  Newer theme (less customization examples)",
            "⚠️  Minimal by design (less visual elements)",
        ],
    },
    "pydata": {
        "name": "PyData Sphinx Theme",
        "description": "Scientific documentation theme based on Bootstrap",
        "config_file": "conf_pydata.py",
        "requirements": ["pydata-sphinx-theme"],
        "pros": [
            "✅ Bootstrap-based responsive design",
            "✅ Great for scientific documentation",
            "✅ Powerful navigation system",
            "✅ Built-in search and indexing",
            "✅ Jupyter integration support",
            "✅ Community-driven development",
        ],
        "cons": [
            "⚠️  Can be heavyweight for simple docs",
            "⚠️  Requires more configuration for customization",
        ],
    },
    "rtd": {
        "name": "Read the Docs (Enhanced)",
        "description": "Classic RTD theme with modern enhancements",
        "config_file": "conf.py",
        "requirements": ["sphinx_rtd_theme"],
        "pros": [
            "✅ Most familiar and widely used",
            "✅ Extensive customization options",
            "✅ Proven reliability and stability",
            "✅ Great documentation and examples",
            "✅ Works well with all Sphinx extensions",
        ],
        "cons": [
            "⚠️  Less modern appearance",
            "⚠️  No built-in dark mode",
            "⚠️  Can look dated compared to newer themes",
        ],
    },
}


def backup_current_config():
    """Backup the current conf.py file."""
    if os.path.exists("conf.py"):
        shutil.copy2("conf.py", "conf_backup.py")
        print("📄 Backed up current conf.py to conf_backup.py")


def check_dependencies(theme_name):
    """Check if theme dependencies are installed."""
    theme = THEMES[theme_name]
    missing_deps = []

    for req in theme["requirements"]:
        try:
            __import__(req.replace("-", "_"))
        except ImportError:
            missing_deps.append(req)

    # Check common dependencies
    common_deps = ["linkify_it_py"]
    for dep in common_deps:
        try:
            __import__(dep)
        except ImportError:
            if "linkify-it-py" not in missing_deps:
                missing_deps.append("linkify-it-py")

    return missing_deps


def install_dependencies(deps):
    """Install missing dependencies."""
    if not deps:
        return True

    print(f"📦 Installing missing dependencies: {', '.join(deps)}")

    try:
        import subprocess

        cmd = [sys.executable, "-m", "pip", "install"] + deps
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def switch_to_theme(theme_name):
    """Switch to the specified theme."""
    if theme_name not in THEMES:
        print(f"❌ Error: Theme '{theme_name}' not found.")
        print(f"Available themes: {', '.join(THEMES.keys())}")
        return False

    theme = THEMES[theme_name]
    config_file = theme["config_file"]

    # Check if theme config file exists
    if not os.path.exists(config_file):
        print(f"❌ Error: Configuration file '{config_file}' not found.")
        print("Please ensure all theme configuration files are present.")
        return False

    # Check and install dependencies
    print("🔍 Checking theme dependencies...")
    missing_deps = check_dependencies(theme_name)

    if missing_deps:
        print(f"⚠️  Missing dependencies: {', '.join(missing_deps)}")
        response = input("Install missing dependencies automatically? (y/n): ")

        if response.lower() in ["y", "yes"]:
            if not install_dependencies(missing_deps):
                print("❌ Failed to install dependencies. Please install manually:")
                for dep in missing_deps:
                    print(f"   pip install {dep}")
                return False
        else:
            print("❌ Cannot switch theme without required dependencies.")
            print("Please install manually:")
            for dep in missing_deps:
                print(f"   pip install {dep}")
            return False
    else:
        print("✅ All dependencies are satisfied!")

    # Backup current configuration
    backup_current_config()

    # Copy theme configuration to conf.py
    shutil.copy2(config_file, "conf.py")

    print(f"🎨 Successfully switched to {theme['name']} theme!")
    print(f"📝 Description: {theme['description']}")
    print(f"⚙️  Configuration: {config_file} → conf.py")

    print(f"\n🏗️  To build with the new theme:")
    print(f"   make html")
    print(f"   # or")
    print(f"   python -m sphinx -b html . _build/html")

    # Test build
    test_response = input("\nTest build the documentation now? (y/n): ")
    if test_response.lower() in ["y", "yes"]:
        print("🔨 Testing build...")
        try:
            import subprocess

            result = subprocess.run(
                [sys.executable, "-m", "sphinx", "-b", "html", ".", "_build/html"],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                print("✅ Test build successful!")
                print("🌐 Open _build/html/index.html to view the documentation")
            else:
                print("⚠️  Build completed with warnings/errors:")
                print(result.stderr[-500:])  # Show last 500 chars of error
        except subprocess.TimeoutExpired:
            print("⏱️  Build taking longer than expected, continuing in background...")
        except Exception as e:
            print(f"❌ Build test failed: {e}")
            print("Please run 'make html' manually to test")

    return True


def list_themes():
    """List all available themes with their descriptions."""
    print("🎨 Available ToolUniverse Documentation Themes:")
    print("=" * 60)

    for theme_key, theme in THEMES.items():
        print(f"\n🎯 {theme['name']} ({theme_key})")
        print(f"   {theme['description']}")
        print(f"   Configuration: {theme['config_file']}")

        if theme["requirements"]:
            print(f"   Requirements: {', '.join(theme['requirements'])}")


def compare_themes():
    """Show a detailed comparison of all themes."""
    print("📊 Theme Comparison")
    print("=" * 80)

    for theme_key, theme in THEMES.items():
        print(f"\n🎨 {theme['name']} ({theme_key})")
        print(f"   {theme['description']}")

        print(f"\n   ✅ Advantages:")
        for pro in theme["pros"]:
            print(f"      {pro}")

        print(f"\n   ⚠️  Considerations:")
        for con in theme["cons"]:
            print(f"      {con}")

        print(f"\n   📦 Installation:")
        if theme["requirements"]:
            for req in theme["requirements"]:
                print(f"      pip install {req}")
        else:
            print(f"      No additional packages required")

        print("-" * 60)


def get_current_theme():
    """Detect the current theme from conf.py."""
    try:
        with open("conf.py", "r") as f:
            content = f.read()
            if "html_theme = 'furo'" in content:
                return "furo"
            elif "html_theme = 'pydata_sphinx_theme'" in content:
                return "pydata"
            elif "html_theme = 'sphinx_rtd_theme'" in content:
                return "rtd"
            else:
                return "unknown"
    except FileNotFoundError:
        return "none"


def show_theme_preview():
    """Show a preview of what each theme looks like."""
    print("🖼️  Theme Preview Guide:")
    print("=" * 50)
    print()
    print("🎨 Furo Theme:")
    print("   • Clean, minimal design with excellent readability")
    print("   • Dark/light mode toggle in top-right corner")
    print("   • Sidebar navigation with smooth animations")
    print("   • Beautiful syntax highlighting with copy buttons")
    print("   • Mobile-first responsive design")
    print()
    print("🎨 PyData Theme:")
    print("   • Bootstrap-based layout with scientific focus")
    print("   • Top navigation bar with dropdown menus")
    print("   • Advanced search functionality")
    print("   • Card-based content organization")
    print("   • Jupyter notebook integration")
    print()
    print("🎨 RTD Theme (Enhanced):")
    print("   • Traditional documentation layout")
    print("   • Left sidebar navigation")
    print("   • Familiar interface for most users")
    print("   • Custom enhancements for better appearance")
    print("   • Extensive customization options")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Switch between ToolUniverse documentation themes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python switch_theme.py furo       # Switch to Furo theme
  python switch_theme.py pydata     # Switch to PyData theme
  python switch_theme.py rtd        # Switch to RTD theme
  python switch_theme.py --list     # List all available themes
  python switch_theme.py --compare  # Compare themes
  python switch_theme.py --preview  # Show theme previews
        """,
    )

    parser.add_argument(
        "theme", nargs="?", choices=list(THEMES.keys()), help="Theme to switch to"
    )

    parser.add_argument(
        "--list", "-l", action="store_true", help="List all available themes"
    )

    parser.add_argument(
        "--compare", "-c", action="store_true", help="Show detailed theme comparison"
    )

    parser.add_argument(
        "--preview", "-p", action="store_true", help="Show theme preview guide"
    )

    parser.add_argument(
        "--current", action="store_true", help="Show currently active theme"
    )

    args = parser.parse_args()

    # Change to docs directory if not already there
    if not os.path.exists("conf.py") and os.path.exists("docs/conf.py"):
        os.chdir("docs")
        print("📁 Changed to docs directory")

    # Show current theme
    if args.current:
        current = get_current_theme()
        if current in THEMES:
            print(f"🎨 Current theme: {THEMES[current]['name']} ({current})")
        else:
            print(f"🎨 Current theme: {current}")
        return

    # List themes
    if args.list:
        list_themes()
        return

    # Compare themes
    if args.compare:
        compare_themes()
        return

    # Show previews
    if args.preview:
        show_theme_preview()
        return

    # Switch theme
    if args.theme:
        current = get_current_theme()
        if current == args.theme:
            print(f"✅ Already using {THEMES[args.theme]['name']} theme")
        else:
            success = switch_to_theme(args.theme)
            if success:
                print(f"\n🔄 Theme changed from {current} to {args.theme}")
                print("\n🚀 Next steps:")
                print("   1. Install required packages (if any)")
                print("   2. Build documentation: make html")
                print("   3. Open _build/html/index.html to preview")
    else:
        # No arguments provided, show help
        parser.print_help()
        print(f"\n🎨 Current theme: {get_current_theme()}")


if __name__ == "__main__":
    main()
