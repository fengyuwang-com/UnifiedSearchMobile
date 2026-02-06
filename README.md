# 一键搜索 - 多平台聚合工具

在多个搜索引擎和AI平台同时提问，一键打开所有结果。

## 📁 文件说明

```
pokers-latest/
├── 一键搜索.exe              ← 可执行文件（双击运行）
├── ai_helper.py              ← Python源代码
├── platforms_config.json     ← 平台配置文件 ⭐ 可编辑
├── GIT_GUIDE.md              ← Git使用指南
├── LICENSE                   ← 许可证
└── README.md                 ← 本说明文件
```

## 🚀 快速开始

1. 双击 `一键搜索.exe`
2. 在输入框输入问题或关键词
3. 勾选想要的平台（默认已勾选5个）
4. 点击"🚀 一键搜索"
5. 浏览器会自动打开所有选中的平台！

## ⚙️ 自定义配置

### 编辑平台配置文件

**文件位置：** `platforms_config.json`

这是一个JSON文件，你可以用记事本或其他文本编辑器打开修改。

### 配置格式示例

```json
{
  "platforms": [
    {
      "id": "perplexity",
      "name": "Perplexity AI",
      "url": "https://www.perplexity.ai/search?q=%query%",
      "type": "ai",
      "description": "AI搜索引擎",
      "enabled": true        ← true=默认勾选, false=默认不勾选
    },
    {
      "id": "google",
      "name": "Google",
      "url": "https://www.google.com/search?q=%query%",
      "type": "search",      ← ai=AI平台, search=搜索引擎
      "description": "谷歌搜索",
      "enabled": true
    }
  ]
}
```

### 修改默认勾选

1. 用记事本打开 `platforms_config.json`
2. 找到你想修改的平台
3. 将 `"enabled": true` 改为 `"enabled": false`（取消默认勾选）
4. 或将 `"enabled": false` 改为 `"enabled": true`（添加默认勾选）
5. 保存文件，重启软件

### 添加新平台

在 `platforms` 数组中添加新项目：

```json
{
  "id": "baidu",
  "name": "百度",
  "url": "https://www.baidu.com/s?wd=%query%",
  "type": "search",
  "description": "百度搜索",
  "enabled": false
}
```

**注意：** `%query%` 是查询占位符，会被自动替换为你输入的问题。

## ✅ 默认勾选的平台

软件首次运行时会自动创建默认配置：

| 平台 | 类型 | 默认勾选 |
|------|------|----------|
| Perplexity AI | AI | ☑️ |
| Google | 搜索 | ☑️ |
| Bing | 搜索 | ☑️ |
| You.com | AI | ☑️ |
| **Bilibili** | 搜索 | ☑️ |
| GitHub | 搜索 | ☐ |
| YouTube | 搜索 | ☐ |
| Ecosia | 搜索 | ☐ |
| ChatGPT | AI | ☐ |
| Claude | AI | ☐ |

## 🎯 使用方法

### 1. 搜索/提问
- 在输入框输入问题（支持多行）
- 点击"🚀 一键搜索"按钮
- 系统会在浏览器中打开所有选中的平台

### 2. 管理平台
- **勾选/取消**：点击复选框启用或禁用平台
- **添加平台**：点击"➕ 添加"按钮
- **编辑平台**：先点击平台名称选中，再点"编辑"
- **删除平台**：先点击平台名称选中，再点"删除"

### 3. 其他功能
- **清空输入**：点击"🗑️ 清空"按钮
- **鼠标滚轮**：在平台列表中使用鼠标滚轮滚动
- **调整窗口**：可以拖动窗口边缘调整大小

## 📱 界面说明

- **窗口大小**：默认 750×600（可调整）
- **最小尺寸**：650×500
- **支持滚轮**：平台列表支持鼠标滚轮滚动
- **自适应布局**：窗口大小改变时自动调整

## 🔧 技术说明

- **开发语言**：Python 3.10
- **GUI框架**：Tkinter
- **工作原理**：通过URL参数将查询传递给各个平台
- **体积**：约 8.5 MB

## 💾 数据文件

软件会自动生成以下文件：

- `platforms_config.json` - 平台配置（**可手动编辑**）
- `query_history.json` - 上次输入的内容
- `operation_log.txt` - 操作日志

**注意：** 这些文件会在第一次运行时自动创建。

## 📝 更新日志

### v2.1 (当前版本)
- ✅ 支持外部JSON配置文件
- ✅ 可以自定义默认勾选的平台
- ✅ 缩小窗口尺寸（750×600）
- ✅ 修复鼠标滚轮滚动问题
- ✅ 调整默认配置：哔哩哔哩勾选，GitHub不勾选

### v2.0
- 合并搜索和AI功能到一个界面
- 支持平台复选框选择
- 默认启用5个平台

## 📄 许可证

MIT License

## 🐛 问题反馈

如有问题，请在GitHub Issues中提出。

---

**提示：** 直接编辑 `platforms_config.json` 文件即可自定义所有平台！
