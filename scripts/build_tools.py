#!/usr/bin/env python3
"""Build ToolUniverse tools."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def main():
    from tooluniverse.generate_tools import main as generate
    
    print("🔧 Building ToolUniverse tools...")
    generate()
    print("✅ Build complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
