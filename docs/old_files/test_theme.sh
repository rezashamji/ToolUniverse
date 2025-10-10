#!/bin/bash
# 测试 Shibuya 主题配置

echo "🔍 Testing Shibuya Theme Configuration"
echo "======================================="
echo ""

# 1. 检查 Python 和 Sphinx
echo "1️⃣ Checking Python and Sphinx..."
python --version
sphinx-build --version
echo ""

# 2. 检查 Shibuya 主题
echo "2️⃣ Checking Shibuya theme..."
python -c "import shibuya; print(f'✅ Shibuya installed: {shibuya.__version__}')" 2>/dev/null || echo "❌ Shibuya NOT installed"
echo ""

# 3. 检查其他必需的包
echo "3️⃣ Checking required packages..."
python -c "import myst_parser; print('✅ myst-parser installed')" 2>/dev/null || echo "❌ myst-parser NOT installed"
python -c "import sphinx_intl; print('✅ sphinx-intl installed')" 2>/dev/null || echo "❌ sphinx-intl NOT installed"
python -c "import sphinx_copybutton; print('✅ sphinx-copybutton installed')" 2>/dev/null || echo "❌ sphinx-copybutton NOT installed"
echo ""

# 4. 检查 conf.py
echo "4️⃣ Checking conf.py..."
if grep -q 'html_theme = "shibuya"' conf.py; then
    echo "✅ Shibuya theme configured in conf.py"
else
    echo "❌ Shibuya theme NOT configured in conf.py"
fi
echo ""

# 5. 检查源文件后缀配置
echo "5️⃣ Checking source_suffix..."
if grep -q '"markdown"' conf.py; then
    echo "✅ Markdown parser configured"
else
    echo "⚠️  Markdown parser might not be configured"
fi
echo ""

# 6. 测试简单构建
echo "6️⃣ Testing simple build..."
echo "Running: sphinx-build -b html . _build/test_html -D language=en"
sphinx-build -b html . _build/test_html -D language=en -q 2>&1 | head -5
if [ -f "_build/test_html/index.html" ]; then
    echo "✅ Build successful!"
    echo "   Output: _build/test_html/index.html"
else
    echo "❌ Build failed!"
fi
echo ""

# 7. 清理
echo "7️⃣ Cleaning up test build..."
rm -rf _build/test_html
echo "✅ Cleanup complete"
echo ""

echo "========================================="
echo "✨ Configuration test complete!"
echo ""
echo "If all checks passed, you can run:"
echo "  ./quick_doc_build.sh"
echo ""
