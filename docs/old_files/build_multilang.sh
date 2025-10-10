#!/bin/bash
# Build documentation in multiple languages

set -e

echo "🌍 Building ToolUniverse documentation in multiple languages..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Clean previous builds
echo -e "${BLUE}🧹 Cleaning previous builds...${NC}"
make clean

# Build English version (default)
echo -e "${BLUE}🇬🇧 Building English documentation...${NC}"
make html
echo -e "${GREEN}✅ English build complete${NC}"

# Update translation files
echo -e "${BLUE}📝 Updating translation files...${NC}"
make gettext
sphinx-intl update -p _build/gettext -l zh_CN
echo -e "${GREEN}✅ Translation files updated${NC}"

# Build Chinese version
echo -e "${BLUE}🇨🇳 Building Chinese documentation...${NC}"
make -e SPHINXOPTS="-D language='zh_CN'" html
mv _build/html _build/html_zh_CN
echo -e "${GREEN}✅ Chinese build complete${NC}"

# Rebuild English version
echo -e "${BLUE}🇬🇧 Rebuilding English documentation...${NC}"
make html
echo -e "${GREEN}✅ English build complete${NC}"

# Create language switcher structure
echo -e "${BLUE}🔗 Creating language switcher structure...${NC}"
mkdir -p _build/html/zh_CN
cp -r _build/html_zh_CN/* _build/html/zh_CN/

# Create a simple language switcher page
cat > _build/html/language_switch.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Language Selection - ToolUniverse</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            text-align: center;
            background: white;
            padding: 3rem;
            border-radius: 1rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
        }
        h1 {
            color: #333;
            margin-bottom: 2rem;
            font-size: 2rem;
        }
        .lang-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }
        .lang-btn {
            display: inline-block;
            padding: 1rem 2rem;
            font-size: 1.2rem;
            text-decoration: none;
            color: white;
            background: #667eea;
            border-radius: 0.5rem;
            transition: all 0.3s;
            font-weight: 600;
        }
        .lang-btn:hover {
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .flag {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌍 Choose Your Language</h1>
        <p>选择您的语言</p>
        <div class="lang-buttons">
            <a href="index.html" class="lang-btn">
                <div class="flag">🇬🇧</div>
                English
            </a>
            <a href="zh_CN/index.html" class="lang-btn">
                <div class="flag">🇨🇳</div>
                简体中文
            </a>
        </div>
    </div>
</body>
</html>
EOF

echo -e "${GREEN}✅ Language switcher created${NC}"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Multi-language build complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📂 Documentation locations:"
echo "   🇬🇧 English:  _build/html/index.html"
echo "   🇨🇳 Chinese:  _build/html/zh_CN/index.html"
echo "   🌍 Switcher: _build/html/language_switch.html"
echo ""
echo "🚀 To view:"
echo "   open _build/html/language_switch.html"
echo ""
echo "📝 To translate:"
echo "   1. Edit files in: locale/zh_CN/LC_MESSAGES/"
echo "   2. Translate msgstr fields"
echo "   3. Run this script again to rebuild"
echo ""
