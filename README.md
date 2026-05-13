[English](README.en.md) | [Español](README.es.md) | [日本語](README.ja.md) | [Français](README.fr.md) | [繁體中文](README.zh-Hant.md)

# 剪贴板搜索 · Clipboard Search for Alfred

基于 Alfred 5 剪贴板历史功能（Powerpack 特性）。

Alfred 自带的剪贴板历史只能按时间顺序浏览，无法按关键字、类型或时间范围检索。本工作流直接读取 Alfred 的剪贴板数据库，提供多维度的搜索和过滤能力，让你在数千条剪贴板记录中快速定位想要的内容。

---

## 功能概览

- **关键字全文搜索**：搜索剪贴板中的文本内容
- **类型过滤**：按文字、图片、文件三种类型筛选
- **时间过滤**：today / yesterday / 最近 N 小时 / N 分钟 / N 天
- **日期过滤**：指定某一天或某个日期范围
- **来源应用过滤**：按产生剪贴板内容的应用筛选
- **组合查询**：以上过滤器可以任意组合
- **快捷键直达**：Cmd+Shift+C 一键唤起搜索界面
- **一键回贴**：Enter 自动粘贴到前台应用光标处
- **Shift 预览**：选中条目后按 Shift 可 Quick Look 预览图片/文件

---

## 安装

### 直接安装（推荐）

```bash
bash Makefile
```

生成 `build/Clipboard Search.alfredworkflow`，双击即用。

### 开发安装

通过软链接安装到 Alfred 工作流目录，修改代码后 `reload` 即可生效，无需反复打包：

```bash
bash link.sh install    # 安装
bash link.sh uninstall  # 卸载
```

---

## 使用说明

### 基础用法

在 Alfred 输入框中输入关键字 `cb`（可在配置中修改），空格后接查询条件。

| 输入 | 效果 |
|---|---|
| `cb` | 显示最近的剪贴板记录（最多 100 条） |
| `cb hello` | 全文搜索包含 "hello" 的剪贴板内容 |

### 类型过滤器

Alfred 将剪贴板历史分为三类：**文字**(0)、**图片**(1)、**文件**(2)。

```
cb :text         只显示文字记录
cb :image        只显示图片记录
cb :file         只显示文件记录
```

`:txt` 与 `:text` 等效，`:img` 与 `:image` 等效。

### 时间过滤器

```
cb :today              今天产生的记录（从 00:00 到当前时刻）
cb :yesterday           昨天产生的记录
cb :2h                  最近 2 小时
cb :30m                 最近 30 分钟
cb :3d                  最近 3 天
```

时间单位：`h`（小时）、`m`（分钟）、`d`（天）。

### 日期过滤器

```
cb :2026-05-10                    完整日期
cb :05-10                         省略年（自动补充当前年份）
cb :2026-05-01..2026-05-10       日期范围
cb :05-01..05-10                  省略年的日期范围
```

### 来源应用过滤器

```
cb @chrome          从 Chrome 中复制的记录
cb @finder          在 Finder 中复制的文件
cb @vscode          从 VS Code 中复制的记录
```

`@` 支持模糊匹配，如 `@chrome` 同时匹配 "Google Chrome" 和 "Google Chrome Dev"。

### 组合查询

所有过滤器可任意组合，空格分隔：

```
cb 关键词 :text :today @chrome
cb :image :today
cb :2026-05-01..2026-05-10 @vscode :text
```

---

## 操作方式

| 操作 | 效果 |
|---|---|
| **Enter** | 自动粘贴到前台应用光标处 |
| **Shift** | Quick Look 预览图片/文件 |
| **Esc** | 关闭搜索界面 |

每条结果显示：
- **标题**：文字首行 / 图片尺寸 / 文件名
- **副标题**：复制时间 · 来源应用 · 类型图标 · 字数 · 行数（文字条目）

---

## 自定义配置

安装后，打开 Alfred 偏好设置 → Workflows → Clipboard Search：

- **关键字**：默认为 `cb`，可改为 `剪贴板` 或拼音缩写 `jtb`
- **快捷键**：默认为 `Cmd+Shift+C`，点击 Hotkey 区域后按下新组合键即可

---

## 工作原理

### 粘贴机制

```
Script Filter → Copy to Clipboard（autopaste=true, vitoclose=true）
```

选中条目后，Alfred 关闭窗口 → 将文字内容复制到剪贴板 → 自动执行 Cmd+V 粘贴到前台应用。粘贴时序由 Alfred 内部控制，不需要手动模拟键盘输入，避免了焦点竞争问题。

文字条目直接将完整内容作为 `arg` 传递给 Copy to Clipboard 输出；图片和文件条目需要在 Alfred 中双击 Copy to Clipboard 节点手动勾选 "Automatically paste to frontmost app" 才能自动粘贴。

### 数据库

直接读取 Alfred 自身的剪贴板数据库：

```
~/Library/Application Support/Alfred/Databases/clipboard.alfdb
```

| 字段 | 说明 |
|---|---|
| `item` | 文字内容 / 图片尺寸信息 / 文件名 |
| `ts` | Mac 绝对时间（2001-01-01 至今的秒数） |
| `app` | 来源应用名称 |
| `dataType` | 0=文字, 1=图片, 2=文件 |
| `dataHash` | 指向 `clipboard.alfdb.data/` 中实际文件的哈希 |

### 依赖

仅使用 Python 3 标准库，无需安装第三方包。

---

## 目录结构

```
alfred/
├── README.md
├── Makefile                            # 构建 .alfredworkflow
├── link.sh                             # 开发安装/卸载
├── .gitignore
└── src/clipboard-search/
    ├── info.plist                      # 工作流配置
    ├── cb_search.py                    # 搜索脚本（Script Filter）
    └── cb_paste.py                     # 复制脚本（图片/文件用）
```

## AI 辅助编程

本项目使用 Claude Code CLI 辅助开发，底层模型为 DeepSeek-V4。主要应用场景：

- **架构设计**：工作流结构、plist 连线配置
- **代码生成**：Python 脚本、正则表达式、AppleScript
- **调试排错**：分析 Alfred Debug 日志定位焦点竞争等隐蔽问题
- **多语言文档**：README 的英文、日文、法文、西班牙文、繁体中文翻译

> Claude Code 是一个 AI 编程助手 CLI 工具，能够读取代码库、运行命令、编辑文件，在多步工作流和跨文件重构场景中特别高效。

## 许可

MIT
