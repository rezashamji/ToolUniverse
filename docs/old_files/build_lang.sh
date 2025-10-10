#!/bin/bash
# ToolUniverse 文档中英文快速切换脚本

set -e

echo "🌍 ToolUniverse Documentation Language Builder"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 显示菜单
echo "请选择操作 / Please select an option:"
echo ""
echo "1) 🇬🇧 构建英文文档 (Build English docs)"
echo "2) 🇨🇳 构建中文文档 (Build Chinese docs)"  
echo "3) 🌏 构建双语文档 (Build both languages)"
echo "4) 📝 更新翻译文件 (Update translation files)"
echo "5) 🌐 打开语言选择页 (Open language switcher)"
echo "6) ❌ 退出 (Exit)"
echo ""

read -p "输入选项 (Enter option) [1-6]: " choice

case $choice in
    1)
        echo ""
        echo "🇬🇧 Building English documentation..."
        make clean
        make html
        echo ""
        echo "✅ English build complete!"
        echo "📂 Location: _build/html/index.html"
        echo ""
        read -p "📖 打开文档？Open docs? (y/n): " open_choice
        if [ "$open_choice" = "y" ] || [ "$open_choice" = "Y" ]; then
            open _build/html/index.html
        fi
        ;;
        
    2)
        echo ""
        echo "🇨🇳 Building Chinese documentation..."
        make clean
        make -e SPHINXOPTS="-D language='zh_CN'" html
        echo ""
        echo "✅ Chinese build complete!"
        echo "📂 Location: _build/html/index.html"
        echo ""
        read -p "📖 打开文档？Open docs? (y/n): " open_choice
        if [ "$open_choice" = "y" ] || [ "$open_choice" = "Y" ]; then
            open _build/html/index.html
        fi
        ;;
        
    3)
        echo ""
        echo "🌏 Building both English and Chinese..."
        
        # Build English
        echo ""
        echo "🇬🇧 Step 1/3: Building English..."
        make clean
        make html
        
        # Build Chinese
        echo ""
        echo "🇨🇳 Step 2/3: Building Chinese..."
        make -e SPHINXOPTS="-D language='zh_CN'" html
        mv _build/html _build/html_zh_CN
        
        # Rebuild English and merge
        echo ""
        echo "🔗 Step 3/3: Merging languages..."
        make html
        mkdir -p _build/html/zh_CN
        cp -r _build/html_zh_CN/* _build/html/zh_CN/
        
        # Create language selector page
        cat > _build/html/languages.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Language Selection - ToolUniverse</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container {
            text-align: center;
            background: white;
            padding: 3rem 2rem;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 1rem;
            font-size: 2.5rem;
            font-weight: 700;
        }
        .subtitle {
            color: #666;
            margin-bottom: 2.5rem;
            font-size: 1.1rem;
        }
        .lang-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }
        .lang-btn {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 1.5rem;
            text-decoration: none;
            color: white;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .lang-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            opacity: 0;
            transition: opacity 0.3s;
        }
        .lang-btn:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        }
        .lang-btn:hover::before {
            opacity: 1;
        }
        .flag {
            font-size: 3rem;
            margin-bottom: 1rem;
            position: relative;
            z-index: 1;
        }
        .lang-name {
            font-size: 1.3rem;
            font-weight: 600;
            position: relative;
            z-index: 1;
        }
        .features {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 2px solid #f0f0f0;
        }
        .feature {
            color: #666;
            margin: 0.5rem 0;
            font-size: 0.95rem;
        }
        @media (max-width: 600px) {
            h1 { font-size: 2rem; }
            .lang-buttons { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌍 ToolUniverse</h1>
        <p class="subtitle">Choose Your Language / 选择您的语言</p>
        
        <div class="lang-buttons">
            <a href="index.html" class="lang-btn">
                <div class="flag">🇬🇧</div>
                <div class="lang-name">English</div>
            </a>
            <a href="zh_CN/index.html" class="lang-btn">
                <div class="flag">🇨🇳</div>
                <div class="lang-name">简体中文</div>
            </a>
        </div>
        
        <div class="features">
            <div class="feature">✨ Beautiful Shibuya Theme</div>
            <div class="feature">🔍 Full-text Search</div>
            <div class="feature">🌓 Dark/Light Mode</div>
            <div class="feature">📱 Mobile Responsive</div>
        </div>
    </div>
</body>
</html>
EOF
        
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "✨ Multi-language build complete!"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "📂 Documentation locations:"
        echo "   🌐 Switcher:  _build/html/languages.html"
        echo "   🇬🇧 English:   _build/html/index.html"
        echo "   🇨🇳 Chinese:   _build/html/zh_CN/index.html"
        echo ""
        read -p "📖 打开语言选择页？Open language switcher? (y/n): " open_choice
        if [ "$open_choice" = "y" ] || [ "$open_choice" = "Y" ]; then
            open _build/html/languages.html
        fi
        ;;
        
    4)
        echo ""
        echo "📝 Updating translation files..."
        make gettext
        sphinx-intl update -p _build/gettext -l zh_CN
        echo ""
        echo "✅ Translation files updated!"
        echo ""
        echo "📁 Translation files location:"
        echo "   locale/zh_CN/LC_MESSAGES/"
        echo ""
        echo "📖 Next steps:"
        echo "   1. Edit .po files in locale/zh_CN/LC_MESSAGES/"
        echo "   2. Fill in msgstr fields with Chinese translations"
        echo "   3. Run this script again and choose option 2 or 3"
        echo ""
        ;;
        
    5)
        echo ""
        if [ -f "_build/html/languages.html" ]; then
            echo "🌐 Opening language switcher..."
            open _build/html/languages.html
        else
            echo "⚠️  Language switcher not found!"
            echo "💡 Please build both languages first (option 3)"
        fi
        ;;
        
    6)
        echo ""
        echo "👋 Goodbye! 再见！"
        exit 0
        ;;
        
    *)
        echo ""
        echo "❌ Invalid option! 无效选项！"
        exit 1
        ;;
esac

echo ""
echo "✨ Done!"
echo ""
