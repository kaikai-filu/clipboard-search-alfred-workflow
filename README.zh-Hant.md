# 剪貼板搜尋 · Clipboard Search for Alfred

Alfred 5 剪貼板歷史增強搜尋工作流（需 Powerpack 授權）。

Alfred 內建的剪貼板歷史只能按時間順序瀏覽，無法按關鍵字、類型或時間範圍檢索。本工作流直接讀取 Alfred 的剪貼板資料庫，提供多維度的搜尋與過濾能力，讓你在數千條剪貼板記錄中快速定位想要的內容。

---

## 功能概覽

- **關鍵字全文搜尋**：搜尋剪貼板中的文字內容
- **類型過濾**：按文字、圖片、檔案三種類型篩選
- **時間過濾**：today / yesterday / 最近 N 小時 / N 分鐘 / N 天
- **日期過濾**：指定某一天或某個日期範圍
- **來源應用過濾**：按產生剪貼板內容的應用篩選
- **組合查詢**：以上過濾器可以任意組合
- **快速鍵直達**：Cmd+Shift+C 一鍵喚起搜尋介面
- **一鍵回貼**：Enter 自動貼上到前景應用游標處
- **Shift 預覽**：選中條目後按 Shift 可 Quick Look 預覽圖片/檔案

---

## 安裝

### 直接安裝（推薦）

```bash
bash Makefile
```

產生 `build/Clipboard Search.alfredworkflow`，雙擊即用。

### 開發安裝

透過軟連結安裝到 Alfred 工作流目錄，修改程式碼後 `reload` 即可生效，無需反覆打包：

```bash
bash link.sh install    # 安裝
bash link.sh uninstall  # 移除
```

---

## 使用說明

### 基礎用法

在 Alfred 輸入框中輸入關鍵字 `cb`（可在設定中修改），空格後接查詢條件。

| 輸入 | 效果 |
|---|---|
| `cb` | 顯示最近的剪貼板記錄（最多 100 條） |
| `cb hello` | 全文搜尋包含 "hello" 的剪貼板內容 |

### 類型過濾器

Alfred 將剪貼板歷史分為三類：**文字**(0)、**圖片**(1)、**檔案**(2)。

```
cb :text         只顯示文字記錄
cb :image        只顯示圖片記錄
cb :file         只顯示檔案記錄
```

`:txt` 與 `:text` 等效，`:img` 與 `:image` 等效。

### 時間過濾器

```
cb :today              今天產生的記錄（從 00:00 到目前時刻）
cb :yesterday           昨天產生的記錄
cb :2h                  最近 2 小時
cb :30m                 最近 30 分鐘
cb :3d                  最近 3 天
```

時間單位：`h`（小時）、`m`（分鐘）、`d`（天）。

### 日期過濾器

```
cb :2026-05-10                    完整日期
cb :05-10                         省略年（自動補充當前年份）
cb :2026-05-01..2026-05-10       日期範圍
cb :05-01..05-10                  省略年的日期範圍
```

### 來源應用過濾器

```
cb @chrome          從 Chrome 中複製的記錄
cb @finder          在 Finder 中複製的檔案
cb @vscode          從 VS Code 中複製的記錄
```

`@` 支援模糊比對，如 `@chrome` 同時比對 "Google Chrome" 和 "Google Chrome Dev"。

### 組合查詢

所有過濾器可任意組合，空格分隔：

```
cb 關鍵詞 :text :today @chrome
cb :image :today
cb :2026-05-01..2026-05-10 @vscode :text
```

---

## 操作方式

| 操作 | 效果 |
|---|---|
| **Enter** | 自動貼上到前景應用游標處 |
| **Shift** | Quick Look 預覽圖片/檔案 |
| **Esc** | 關閉搜尋介面 |

每條結果顯示：
- **標題**：文字首行 / 圖片尺寸 / 檔案名稱
- **副標題**：複製時間 · 來源應用 · 類型圖示

---

## 自訂設定

安裝後，開啟 Alfred 偏好設定 → Workflows → Clipboard Search：

- **關鍵字**：預設為 `cb`，可改為中文或拼音縮寫
- **快速鍵**：預設為 `Cmd+Shift+C`，點擊 Hotkey 區域後按下新組合鍵即可

---

## 工作原理

### 貼上機制

```
Script Filter → Copy to Clipboard（autopaste=true, vitoclose=true）
```

選中條目後，Alfred 關閉視窗 → 將文字內容複製到剪貼板 → 自動執行 Cmd+V 貼上到前景應用。貼上時序由 Alfred 內部控制，不需要手動模擬鍵盤輸入，避免了焦點競爭問題。

### 資料庫

直接讀取 Alfred 自身的剪貼板資料庫：

```
~/Library/Application Support/Alfred/Databases/clipboard.alfdb
```

| 欄位 | 說明 |
|---|---|
| `item` | 文字內容 / 圖片尺寸資訊 / 檔案名稱 |
| `ts` | Mac 絕對時間（2001-01-01 至今的秒數） |
| `app` | 來源應用名稱 |
| `dataType` | 0=文字, 1=圖片, 2=檔案 |
| `dataHash` | 指向 `clipboard.alfdb.data/` 中實際檔案的雜湊值 |

### 依賴

僅使用 Python 3 標準庫，無需安裝第三方套件。

---

## 目錄結構

```
alfred/
├── README.md
├── Makefile                            # 構建 .alfredworkflow
├── link.sh                             # 開發安裝/移除
├── .gitignore
└── src/clipboard-search/
    ├── info.plist                      # 工作流設定
    ├── cb_search.py                    # 搜尋腳本（Script Filter）
    └── cb_paste.py                     # 複製腳本（圖片/檔案用）
```

## 許可

MIT
