# 🌍 ToolUniverse 中英文文档系统

## ✨ 功能特性

- ✅ **完整的中英文支持** - 使用 Sphinx i18n 系统
- ✅ **Shibuya 现代主题** - 美观的界面，完美的侧边栏导航
- ✅ **浮动语言切换器** - 页面右下角，随时切换语言
- ✅ **独立语言选择页** - 优雅的语言选择界面
- ✅ **深色/浅色模式** - 自动适配系统主题
- ✅ **移动端优化** - 响应式设计

## 🚀 快速开始

### 方法 1: 使用交互式脚本（推荐）

```bash
cd docs
./build_lang.sh
```

然后选择：
1. 构建英文文档
2. 构建中文文档
3. 构建双语文档（推荐）
4. 更新翻译文件
5. 打开语言选择页

### 方法 2: 直接命令

```bash
# 构建英文版
make html

# 构建中文版
make -e SPHINXOPTS="-D language='zh_CN'" html

# 更新翻译
make gettext
sphinx-intl update -p _build/gettext -l zh_CN
```

## 📝 如何翻译

### 1. 生成/更新翻译文件

```bash
./build_lang.sh
# 选择选项 4
```

### 2. 编辑翻译文件

翻译文件位置：`locale/zh_CN/LC_MESSAGES/*.po`

示例（`locale/zh_CN/LC_MESSAGES/index.po`）：

```text
msgid "🚀 Getting Started"
msgstr "🚀 快速开始"

msgid "🤖 Building AI Scientists"  
msgstr "🤖 构建 AI 科学家"

msgid "🔧 Tools"
msgstr "🔧 工具"
```

### 3. 重新构建

```bash
./build_lang.sh
# 选择选项 2 (中文) 或 3 (双语)
```

## 📂 文件结构

```
docs/
├── conf.py                      # Sphinx 配置（Shibuya 主题）
├── build_lang.sh                # 交互式语言构建脚本
├── build_multilang.sh           # 完整双语构建脚本
├── quick_build_zh.sh            # 快速中文构建
├── I18N_GUIDE.md               # 详细翻译指南
│
├── locale/
│   └── zh_CN/
│       └── LC_MESSAGES/
│           ├── index.po         # 首页翻译
│           ├── quickstart.po    # 快速开始翻译
│           └── ...              # 其他页面翻译
│
├── _static/
│   ├── language_switcher.css   # 语言切换器样式
│   └── language_switcher.js    # 语言切换器脚本
│
└── _build/
    └── html/
        ├── index.html           # 英文首页
        ├── languages.html       # 语言选择页
        └── zh_CN/
            └── index.html       # 中文首页
```

## 🎨 主题特性

### Shibuya 主题配置

```python
# conf.py
html_theme = "shibuya"
html_theme_options = {
    "dark_mode": True,
    "globaltoc_expand_depth": 2,
    "language_switch": {
        "zh_CN": "简体中文",
        "en": "English",
    },
}
```

### 侧边栏导航

- ✅ 自动生成导航树
- ✅ 可折叠章节
- ✅ 高亮当前页面
- ✅ 深度可配置

### 顶部导航

- 🏠 Home
- 📖 User Guide  
- 🔧 Tools
- 🎯 Tutorials
- 🔍 Search

## 🌐 语言切换方式

### 1. 浮动切换器（所有页面）

页面右下角的下拉菜单：
- 🇬🇧 English
- 🇨🇳 简体中文

### 2. 语言选择页

访问 `_build/html/languages.html` 或运行：

```bash
./build_lang.sh
# 选择选项 5
```

### 3. 直接 URL

- 英文：`/index.html`
- 中文：`/zh_CN/index.html`

## 📊 翻译进度

### 已翻译

✅ 首页导航章节标题：
- 🚀 快速开始
- 🤖 构建 AI 科学家  
- 🔧 工具
- 💡 使用 ToolUniverse
- 🔨 扩展 ToolUniverse
- 🔌 API 参考
- ❓ 参考资料

### 待翻译

需要翻译的主要文件（按优先级）：

1. ☐ `quickstart.po` - 快速开始
2. ☐ `installation.po` - 安装指南
3. ☐ `getting_started.po` - 入门教程
4. ☐ `faq.po` - 常见问题
5. ☐ `guide/*.po` - 用户指南
6. ☐ `tools/*.po` - 工具文档
7. ☐ `tutorials/*.po` - 教程
8. ☐ `api/*.po` - API 参考

## 🛠️ 开发工作流

### 添加新内容

1. 编辑 `.rst` 或 `.md` 文件
2. 构建英文版测试
3. 生成翻译模板
4. 翻译中文
5. 构建中文版测试

```bash
# 编辑文档...
make html                        # 测试英文
make gettext                     # 生成模板
sphinx-intl update -l zh_CN      # 更新翻译
# 编辑 .po 文件...
./build_lang.sh                  # 选择选项 3
```

### 批量翻译技巧

使用 AI 辅助翻译：

```bash
# 提取所有 msgid
grep 'msgid' locale/zh_CN/LC_MESSAGES/index.po

# 使用 ChatGPT/Claude 批量翻译
# 然后替换 msgstr 字段
```

## 📖 相关文档

- [I18N_GUIDE.md](I18N_GUIDE.md) - 详细翻译指南
- [Sphinx i18n 文档](https://www.sphinx-doc.org/en/master/usage/advanced/intl.html)
- [Shibuya 主题文档](https://shibuya.lepture.com/)
- [sphinx-intl 文档](https://pypi.org/project/sphinx-intl/)

## ❓ 常见问题

### Q: 翻译后看不到效果？

A: 确保：
1. `.po` 文件已保存
2. 运行 `make clean`
3. 重新构建对应语言版本

### Q: 如何只翻译部分页面？

A: 可以！只翻译对应的 `.po` 文件，未翻译的会显示英文原文。

### Q: 语言切换器不显示？

A: 检查：
1. `_static/language_switcher.js` 和 `.css` 文件存在
2. `conf.py` 中正确配置了 `html_js_files` 和 `html_css_files`
3. 浏览器控制台是否有错误

### Q: 如何部署多语言文档？

A: 
```bash
# 构建双语版本
./build_lang.sh  # 选择选项 3

# 部署整个 _build/html 目录
# 目录结构：
# /index.html          (英文)
# /zh_CN/index.html    (中文)
# /languages.html      (语言选择)
```

## 🚀 部署

### GitHub Pages

```yaml
# .github/workflows/docs.yml
- name: Build multi-language docs
  run: |
    cd docs
    pip install sphinx-intl shibuya
    ./build_lang.sh <<< "3"  # 自动选择选项 3
    
- name: Deploy
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./docs/_build/html
```

### 自定义服务器

```bash
# 构建
./build_lang.sh <<< "3"

# 复制到服务器
scp -r _build/html/* user@server:/var/www/docs/
```

## 📝 TODO

- [ ] 完成所有主要页面的中文翻译
- [ ] 添加更多语言（日语、韩语等）
- [ ] 自动化翻译工作流
- [ ] CI/CD 集成
- [ ] 翻译进度追踪

## 💡 贡献

欢迎贡献翻译！

1. Fork 项目
2. 编辑 `locale/zh_CN/LC_MESSAGES/*.po`
3. 提交 Pull Request

## 📄 许可

与 ToolUniverse 项目保持一致。

---

🌟 **现在就开始使用双语文档吧！**

```bash
cd docs
./build_lang.sh
```
