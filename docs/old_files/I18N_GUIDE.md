# ToolUniverse 文档中英文切换指南

## 📋 概述

ToolUniverse 文档现已支持中英文切换！本指南将帮助你完成翻译和构建。

## 🚀 快速开始

### 1. 构建多语言文档

```bash
cd docs
./build_multilang.sh
```

这将自动：
- 生成英文文档
- 生成中文文档（基于翻译）
- 创建语言切换器页面

### 2. 查看效果

```bash
open _build/html/language_switch.html
```

## 📝 如何翻译

### 翻译文件位置

所有翻译文件在：`locale/zh_CN/LC_MESSAGES/`

### 翻译格式示例

打开 `locale/zh_CN/LC_MESSAGES/index.po`：

```po
# 原文
msgid "🚀 Getting Started"
# 在这里填写中文翻译
msgstr "🚀 快速开始"

msgid "🤖 Building AI Scientists"
msgstr "🤖 构建 AI 科学家"

msgid "🔧 Tools"
msgstr "🔧 工具"

msgid "💡 Use ToolUniverse"
msgstr "💡 使用 ToolUniverse"

msgid "🔨 Expand ToolUniverse"
msgstr "🔨 扩展 ToolUniverse"

msgid "🔌 API"
msgstr "🔌 API"

msgid "❓ Reference"
msgstr "❓ 参考"
```

### 主要翻译文件

优先翻译以下文件以获得最佳效果：

1. **首页导航** - `locale/zh_CN/LC_MESSAGES/index.po`
2. **快速开始** - `locale/zh_CN/LC_MESSAGES/quickstart.po`
3. **安装指南** - `locale/zh_CN/LC_MESSAGES/installation.po`
4. **入门教程** - `locale/zh_CN/LC_MESSAGES/getting_started.po`
5. **FAQ** - `locale/zh_CN/LC_MESSAGES/faq.po`

## 🔄 工作流程

### 完整翻译流程

```bash
# 1. 更新翻译模板（当源文档有变化时）
make gettext
sphinx-intl update -p _build/gettext -l zh_CN

# 2. 编辑翻译文件
# 打开 locale/zh_CN/LC_MESSAGES/*.po 文件
# 填写 msgstr "" 中的中文翻译

# 3. 构建多语言文档
./build_multilang.sh

# 4. 预览
open _build/html/language_switch.html
```

### 快速测试单个文件翻译

```bash
# 只构建中文版本
make -e SPHINXOPTS="-D language='zh_CN'" html

# 查看结果
open _build/html/index.html
```

## 📂 目录结构

```
docs/
├── locale/
│   └── zh_CN/
│       └── LC_MESSAGES/
│           ├── index.po          # 首页翻译
│           ├── quickstart.po     # 快速开始翻译
│           ├── installation.po   # 安装指南翻译
│           └── ...               # 其他页面翻译
├── _build/
│   ├── html/                     # 英文文档
│   │   ├── index.html
│   │   └── zh_CN/                # 中文文档
│   │       └── index.html
│   └── gettext/                  # 翻译模板
└── build_multilang.sh            # 多语言构建脚本
```

## 🎯 Shibuya 主题语言切换器

Shibuya 主题已配置语言切换器：

```python
# conf.py
html_theme_options = {
    "language_switch": {
        "zh_CN": "简体中文",
        "en": "English",
    },
}
```

当有多个语言版本时，主题会自动在导航栏显示语言切换下拉菜单。

## 💡 翻译技巧

### 1. 批量翻译

使用文本编辑器的查找替换功能：
- VSCode: Cmd+Shift+H
- Vim: `:%s/msgstr ""/msgstr "翻译"/g`

### 2. 保持格式

翻译时保持：
- Emoji 图标不变
- Markdown 语法不变
- reStructuredText 指令不变
- 代码块不变

### 3. 使用翻译工具

可以使用：
- DeepL Translator
- Google Translate
- ChatGPT/Claude

然后手动审核调整。

### 4. 渐进式翻译

不需要一次翻译所有文件：
1. 先翻译首页和主要导航
2. 再翻译快速开始和安装
3. 最后翻译详细文档和 API

未翻译的内容会显示英文原文。

## 🔧 配置详解

### conf.py 国际化配置

```python
# 语言设置
language = "en"  # 默认语言

# i18n 设置
locale_dirs = ["locale/"]  # 翻译文件目录
gettext_compact = False     # 每个文档独立翻译文件
gettext_uuid = True         # 使用 UUID 标识
gettext_location = True     # 在翻译文件中包含位置信息
gettext_auto_build = True   # 自动构建翻译

# 支持的语言
languages = {
    "en": "English",
    "zh_CN": "简体中文",
}
```

## 🌐 部署多语言文档

### GitHub Pages

```yaml
# .github/workflows/docs.yml
- name: Build multi-language docs
  run: |
    cd docs
    ./build_multilang.sh
    
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./docs/_build/html
```

### 自定义域名语言路径

- 英文: `https://yourdomain.com/`
- 中文: `https://yourdomain.com/zh_CN/`

## 📚 参考资源

- [Sphinx 国际化文档](https://www.sphinx-doc.org/en/master/usage/advanced/intl.html)
- [sphinx-intl 使用指南](https://pypi.org/project/sphinx-intl/)
- [Shibuya 主题文档](https://shibuya.lepture.com/)

## ❓ 常见问题

### Q: 翻译后重新构建没有生效？

A: 确保：
1. .po 文件已保存
2. 运行 `make clean` 清理缓存
3. 重新运行 `./build_multilang.sh`

### Q: 如何只更新某个页面的翻译？

A: 
```bash
# 更新特定文件的翻译模板
make gettext
sphinx-intl update -p _build/gettext -l zh_CN
# 只编辑对应的 .po 文件
```

### Q: 可以添加其他语言吗？

A:可以！修改 conf.py：
```python
languages = {
    "en": "English",
    "zh_CN": "简体中文",
    "ja": "日本語",  # 添加日语
}
```

然后运行：
```bash
sphinx-intl update -p _build/gettext -l ja
```

## 🎉 开始翻译

准备好了吗？运行以下命令开始：

```bash
cd docs
./build_multilang.sh
```

Happy translating! 🌍
