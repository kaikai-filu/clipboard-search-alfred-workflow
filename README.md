# 剪贴板搜索 · Clipboard Search for Alfred

Alfred 5 剪贴板历史增强搜索工作流（需 Powerpack 授权）。

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
- **一键回贴**：Enter 将选中项重新复制到系统剪贴板
- **预览支持**：Cmd+Enter 对图片/文件进行 Quick Look 预览

---

## 安装

### 方式一：开发安装（推荐日常使用）

通过软链接将工作流安装到 Alfred 的工作流目录，修改代码后直接生效，无需重复打包：

```bash
# 安装（创建软链接）
bash link.sh install

# 卸载（删除软链接）
bash link.sh uninstall
```

安装后在 Alfred 中重新加载工作流即可生效。

### 方式二：打包安装（推荐分发）

生成 `.alfredworkflow` 文件，双击即可安装：

```bash
bash Makefile
# 生成文件: build/Clipboard Search.alfredworkflow
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

按剪贴板内容的数据类型筛选。Alfred 将剪贴板历史分为三类：

- **文字** (dataType=0)：纯文本、富文本、URL、代码片段等
- **图片** (dataType=1)：截图、复制的图片等
- **文件** (dataType=2)：在 Finder 中复制的文件

```
cb :text         只显示文字记录
cb :image        只显示图片记录
cb :file         只显示文件记录
```

`:` 是过滤器的前缀符号，`:txt` 与 `:text` 等效，`:img` 与 `:image` 等效。

### 时间过滤器

```
cb :today              今天产生的记录（从 00:00 到当前时刻）
cb :yesterday           昨天产生的记录
cb :2h                  最近 2 小时
cb :30m                 最近 30 分钟
cb :3d                  最近 3 天
```

可用的时间单位：`h`（小时）、`m`（分钟）、`d`（天）。

### 日期过滤器

```
cb :2026-05-10                    2026 年 5 月 10 日当天的记录
cb :2026-05-01..2026-05-10       5 月 1 日至 5 月 10 日之间的记录
```

日期格式为 `YYYY-MM-DD`，范围用 `..` 连接。

### 来源应用过滤器

```
cb @chrome          从 Google Chrome 中复制的记录
cb @finder          在 Finder 中复制的文件
cb @vscode          从 Visual Studio Code 中复制的记录
```

`@` 是应用过滤器的前缀符号，支持模糊匹配（如 `@chrome` 同时匹配 "Google Chrome" 和 "Google Chrome Dev"）。

> 来源应用名称来自 Alfred 记录的 `app` 字段，可以使用 Alfred 自带的剪贴板历史查看各应用的实际名称。

### 组合查询

所有过滤器可以任意组合使用，空格分隔：

```
cb 搜索关键词 :text :today @chrome         今天在 Chrome 中复制的包含"搜索关键词"的文字
cb :image :today                            今天复制的所有图片
cb :file :yesterday                         昨天复制的所有文件
cb :2026-05-01..2026-05-10 @vscode :text   5 月上旬在 VS Code 中复制的文字
```

---

## 操作方式

在搜索结果中：

| 操作 | 效果 |
|---|---|
| **Enter** | 将选中项复制到系统剪贴板，可直接 Cmd+V 粘贴 |
| **Cmd+Enter** | Quick Look 预览（对图片和文件类型特别有用） |
| **Esc** | 关闭搜索界面 |

每条结果显示：
- **标题**：文字的首行内容 / 图片尺寸信息 / 文件名
- **副标题**：复制时间 · 来源应用 · 类型图标

---

## 自定义配置

安装后，打开 Alfred 偏好设置 → Workflows → Clipboard Search，可以修改：

### 关键字

修改触发搜索的关键字（默认为 `cb`）。如果你习惯用中文，可以改为 `剪贴板` 或拼音缩写 `jtb`。

### 快捷键

修改快捷键（默认为 `Cmd+Shift+C`）。点击 Hotkey 区域后按下你想要的组合键即可。

> 如果快捷键与其他软件冲突，Alfred 会显示警告。建议选择一个不常用的组合键。

---

## 工作原理

本工作流直接读取 Alfred 自身的剪贴板数据库，不依赖任何第三方工具或 API。

### 数据库位置

```
~/Library/Application Support/Alfred/Databases/clipboard.alfdb
```

### 数据库结构

| 字段 | 说明 |
|---|---|
| `item` | 内容本体（文字则为全文，图片为尺寸/大小信息，文件为文件名） |
| `ts` | 时间戳（Mac 绝对时间，即 2001-01-01 至今的秒数） |
| `app` | 来源应用名称 |
| `apppath` | 来源应用路径 |
| `dataType` | 类型：0=文字, 1=图片, 2=文件 |
| `dataHash` | 数据哈希值，指向 `clipboard.alfdb.data/` 中的实际文件 |

### 图片与文件数据

- 文字内容直接存储在 `item` 字段中
- 图片以 TIFF 格式存储在 `clipboard.alfdb.data/` 目录，文件名是哈希值
- 文件引用以 `.plist` 文件存储在 `clipboard.alfdb.data/` 目录，内容为原始文件路径

### 依赖

仅使用 Python 3 标准库（`json`、`sqlite3`、`re`、`datetime`、`subprocess`），无需安装任何第三方包。

---

## 常见问题

**Q: 搜索不到某些剪贴板记录？**

Alfred 默认只保留最近 3 个月的剪贴板历史。可以在 Alfred 偏好设置 → Features → Clipboard History 中调整保留时间。此外，Alfred 不会记录密码管理器等标记为"安全输入"的应用中的内容。

**Q: 图片无法复制回剪贴板？**

图片的粘贴使用了 macOS 的 NSImage API，部分特殊格式（如 SVG、动画 GIF）可能无法以图片形式粘贴。此时可以先用 Cmd+Enter 预览确认图片内容。

**Q: 原始文件已被删除，文件记录还有用吗？**

如果文件已被移动或删除，粘贴文件引用会失败。但你可以从剪贴板历史中看到文件名和路径，方便定位。

**Q: 搜索结果为什么最多只有 100 条？**

为避免 Alfred 界面响应变慢，单次查询最多返回 100 条记录。你可以通过更精确的过滤器缩小范围。

**Q: 如何修改最大返回数量？**

编辑 `src/clipboard-search/cb_search.py`，修改第 20 行的 `MAX_RESULTS = 100` 为其他数值。

---

## 目录结构

```
alfred/
├── README.md                           # 本文件
├── Makefile                            # 构建 .alfredworkflow 分发包
├── link.sh                             # 开发安装 / 卸载脚本
└── src/clipboard-search/
    ├── info.plist                      # Alfred 工作流配置（关键字、快捷键、连线）
    ├── cb_search.py                    # 搜索脚本（解析查询、查数据库、输出 Alfred JSON）
    └── cb_paste.py                     # 粘贴脚本（根据类型将内容复制到系统剪贴板）
```

## 许可

MIT
