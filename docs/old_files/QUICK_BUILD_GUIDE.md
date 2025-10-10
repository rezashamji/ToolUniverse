# 🚀 ToolUniverse 文档快速构建指南

## ✨ 一键构建中英文文档

现在 `quick_doc_build.sh` 和 `quick_doc_build_cn.sh` 脚本会**自动构建中英文两个版本**！

## 📝 使用方法

### 方法 1: 默认构建（中英文）

```bash
cd docs
./quick_doc_build.sh
# 或
./quick_doc_build_cn.sh
```

**自动执行：**
- ✅ 生成工具配置索引
- ✅ 生成 Remote Tools 文档
- ✅ 构建英文文档 → `_build/html/en/`
- ✅ 更新中文翻译
- ✅ 构建中文文档 → `_build/html/zh-CN/`
- ✅ 创建语言选择页 → `_build/html/index.html`
- ✅ 启动本地服务器（可选）

### 方法 2: 仅构建英文

```bash
DOC_LANGUAGES=en ./quick_doc_build.sh
```

### 方法 3: 仅构建中文

```bash
DOC_LANGUAGES=zh_CN ./quick_doc_build.sh
```

### 方法 4: 自定义语言组合

```bash
DOC_LANGUAGES="en,zh_CN,ja" ./quick_doc_build.sh
```

## 📂 构建结果

构建完成后，文档结构如下：

```
_build/html/
├── index.html          # 🌍 语言选择页（多语言时自动创建）
├── en/                 # 🇬🇧 英文文档
│   ├── index.html
│   ├── api/
│   └── ...
└── zh-CN/              # 🇨🇳 中文文档
    ├── index.html
    ├── api/
    └── ...
```

## 🌐 访问文档

### 浏览器访问

构建完成后，脚本会显示访问链接：

```
📂 Access documentation:
   🌍 Language Switcher: file:///path/to/_build/html/index.html

   🇬🇧 English:
      📖 Home: file:///path/to/_build/html/en/index.html
      🔧 API:  file:///path/to/_build/html/en/api/modules.html

   🇨🇳 简体中文:
      📖 Home: file:///path/to/_build/html/zh-CN/index.html
      🔧 API:  file:///path/to/_build/html/zh-CN/api/modules.html
```

### 本地服务器

脚本会询问是否启动本地服务器：

```
Start local server to view documentation? (y/n)
```

选择 `y` 后，访问：
- 🌍 语言选择：`http://localhost:8080/index.html`
- 🇬🇧 英文：`http://localhost:8080/en/index.html`
- 🇨🇳 中文：`http://localhost:8080/zh-CN/index.html`

## 🔧 环境变量配置

### 语言设置

```bash
# 默认：中英文
DOC_LANGUAGES="en,zh_CN" ./quick_doc_build.sh

# 仅英文
DOC_LANGUAGES="en" ./quick_doc_build.sh

# 仅中文
DOC_LANGUAGES="zh_CN" ./quick_doc_build.sh

# 添加更多语言
DOC_LANGUAGES="en,zh_CN,ja,ko" ./quick_doc_build.sh
```

### 其他选项

```bash
# 跳过 Remote Tools 文档生成
DOC_SKIP_REMOTE=1 ./quick_doc_build.sh

# 跳过服务器启动提示
DOC_SKIP_SERVER_PROMPT=1 ./quick_doc_build.sh

# 严格模式（警告视为错误）
DOCS_STRICT=1 ./quick_doc_build.sh

# 组合使用
DOC_LANGUAGES="en,zh_CN" DOC_SKIP_SERVER_PROMPT=1 ./quick_doc_build.sh
```

## 📝 翻译工作流

### 1. 构建时自动更新翻译文件

每次运行脚本时，如果包含中文（`zh_CN`），会自动：
- 提取最新的可翻译文本 → `_build/gettext/`
- 更新翻译文件 → `locale/zh_CN/LC_MESSAGES/*.po`

### 2. 编辑翻译

```bash
# 打开翻译文件
vi locale/zh_CN/LC_MESSAGES/index.po
vi locale/zh_CN/LC_MESSAGES/quickstart.po
# ... 其他文件
```

翻译格式：
```po
msgid "Getting Started"
msgstr "快速开始"

msgid "Installation"
msgstr "安装指南"
```

### 3. 重新构建

```bash
./quick_doc_build.sh
```

翻译会自动应用到中文版本！

## 🎨 主题特性

### Shibuya 现代主题

- ✅ 美观的界面设计
- ✅ 完整的左侧导航栏
- ✅ 深色/浅色模式切换
- ✅ 移动端响应式
- ✅ 内置搜索功能

### 语言切换

- 🌍 多语言索引页（优雅的语言选择界面）
- 🔄 各语言版本独立完整
- 📱 所有设备完美适配

## 🚀 快速开始

第一次使用？就这么简单：

```bash
cd /Users/shgao/logs/25.05.28tooluniverse/ToolUniverse/docs
./quick_doc_build.sh
```

等待构建完成后：
1. 选择 `y` 启动本地服务器
2. 浏览器会显示语言选择页
3. 选择你想要的语言
4. 享受阅读！📖

## 💡 Tips

### 加快构建速度

```bash
# 仅构建一种语言
DOC_LANGUAGES=en ./quick_doc_build.sh

# 跳过 Remote Tools
DOC_SKIP_REMOTE=1 ./quick_doc_build.sh
```

### CI/CD 集成

```bash
# GitHub Actions / CI 环境
CI=1 ./quick_doc_build.sh
# 会自动跳过服务器启动
```

### 清理缓存

```bash
# 清理构建缓存
rm -rf _build/

# 重新完整构建
./quick_doc_build.sh
```

## 📚 更多文档

- [I18N_GUIDE.md](I18N_GUIDE.md) - 详细翻译指南
- [MULTILANG_README.md](MULTILANG_README.md) - 多语言系统说明
- [build_lang.sh](build_lang.sh) - 交互式语言构建脚本

## ❓ 常见问题

### Q: 为什么看不到中文翻译？

A: 检查：
1. `locale/zh_CN/LC_MESSAGES/` 目录中的 `.po` 文件是否有翻译内容
2. `.po` 文件中 `msgstr` 是否填写了中文
3. 重新运行构建脚本

### Q: 如何只看英文或中文？

A: 使用环境变量：
```bash
DOC_LANGUAGES=en ./quick_doc_build.sh    # 仅英文
DOC_LANGUAGES=zh_CN ./quick_doc_build.sh # 仅中文
```

### Q: 构建很慢怎么办？

A: 
- 跳过 Remote Tools：`DOC_SKIP_REMOTE=1`
- 只构建一种语言：`DOC_LANGUAGES=en`

### Q: 如何部署到服务器？

A: 
```bash
# 构建文档
./quick_doc_build.sh

# 上传整个 _build/html 目录
scp -r _build/html/* user@server:/var/www/docs/
```

## 🎉 开始使用

现在就试试吧！

```bash
cd docs
./quick_doc_build.sh
```

一键生成精美的中英文文档！🚀
