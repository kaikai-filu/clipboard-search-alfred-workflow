# クリップボード検索 · Clipboard Search for Alfred

Alfred 5 用クリップボード履歴拡張検索ワークフロー（Powerpack ライセンス必須）。

Alfred 標準のクリップボードビューアを超えて、キーワード、タイプ、時間、日付、ソースアプリケーションで数千件のエントリを検索・フィルタリングできます。

---

## 機能

- **キーワード検索** — クリップボード履歴の全文検索
- **タイプフィルタ** — `:text` `:image` `:file`
- **時間フィルタ** — `:today` `:yesterday` `:2h` `:30m` `:3d`
- **日付フィルタ** — `:2026-05-10` `:05-10`（年省略可）または範囲指定
- **アプリフィルタ** — `@chrome` `@finder` `@vscode`
- **組み合わせ検索** — すべてのフィルタを自由に組み合わせ可能
- **ホットキー** — Cmd+Shift+C でクイックアクセス
- **自動ペースト** — Enter で最前面のアプリケーションに直接貼り付け
- **Quick Look** — Shift で画像やファイルをプレビュー

---

## インストール

### 直接インストール（推奨）

```bash
bash Makefile
```

生成された `build/Clipboard Search.alfredworkflow` をダブルクリック。

### 開発用インストール

Alfred のワークフローディレクトリにシンボリックリンクを作成：

```bash
bash link.sh install    # インストール
bash link.sh uninstall  # アンインストール
```

---

## 使い方

### 基本

Alfred で `cb`（変更可）と入力し、続けて検索条件を入力します。

| 入力 | 結果 |
|---|---|
| `cb` | 最近のエントリを表示（最大100件） |
| `cb hello` | "hello" を含むエントリを全文検索 |

### タイプフィルタ

```
cb :text         テキストのみ
cb :image        画像のみ
cb :file         ファイルのみ
```

`:txt` = `:text`, `:img` = `:image`。

### 時間フィルタ

```
cb :today              今日のエントリ
cb :yesterday           昨日のエントリ
cb :2h                  過去2時間
cb :30m                 過去30分
cb :3d                  過去3日間
```

単位：`h`（時間）、`m`（分）、`d`（日）。

### 日付フィルタ

```
cb :2026-05-10                    完全な日付
cb :05-10                         短縮日付（今年と見なす）
cb :2026-05-01..2026-05-10       日付範囲
cb :05-01..05-10                  短縮日付範囲
```

### アプリフィルタ

```
cb @chrome          Chrome から
cb @finder          Finder から
cb @vscode          VS Code から
```

`@` はあいまい一致に対応（例：`@chrome` は "Google Chrome" と "Google Chrome Dev" の両方に一致）。

### 組み合わせ検索

```
cb キーワード :text :today @chrome
cb :image :today
cb :2026-05-01..2026-05-10 @vscode :text
```

---

## 操作

| キー | 動作 |
|---|---|
| **Enter** | 最前面アプリに自動ペースト |
| **Shift** | Quick Look プレビュー |
| **Esc** | Alfred を閉じる |

各結果の表示：
- **タイトル**：テキストの先頭行 / 画像サイズ / ファイル名
- **サブタイトル**：タイムスタンプ · ソースアプリ · タイプアイコン

---

## 設定

Alfred 環境設定 → Workflows → Clipboard Search：

- **キーワード**：デフォルト `cb`
- **ホットキー**：デフォルト `Cmd+Shift+C`

---

## 仕組み

### ペーストメカニズム

```
Script Filter → Copy to Clipboard（autopaste=true, vitoclose=true）
```

Alfred がウィンドウを閉じる → テキストをクリップボードにコピー → Cmd+V を自動実行。タイミングは Alfred が内部で制御するため、フォーカスの競合が発生しません。

### データベース

Alfred 自身のクリップボードデータベースを直接読み取ります：

```
~/Library/Application Support/Alfred/Databases/clipboard.alfdb
```

| カラム | 説明 |
|---|---|
| `item` | テキスト内容 / 画像情報 / ファイル名 |
| `ts` | Mac 絶対時間（2001-01-01 からの秒数） |
| `app` | ソースアプリケーション名 |
| `dataType` | 0=テキスト, 1=画像, 2=ファイル |
| `dataHash` | `clipboard.alfdb.data/` 内のファイルを示すハッシュ |

### 依存関係

Python 3 標準ライブラリのみ — サードパーティパッケージ不要。

---

## 構造

```
alfred/
├── README.md
├── Makefile
├── link.sh
├── .gitignore
└── src/clipboard-search/
    ├── info.plist
    ├── cb_search.py
    └── cb_paste.py
```

## ライセンス

MIT
