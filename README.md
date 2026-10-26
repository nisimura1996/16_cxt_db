# LLM Wiki (16_cxt_db)

Andrej Karpathy（アンドレイ・カルパシー）が提唱した設計思想に基づき、**「客観的知識（世の中の事実）」**と**「主観的知識（じぶん取説・お作法）」**を同一ワークスペースで共存・運用する永続的ナレッジベースです。

---

## 📂 ディレクトリ構成（ソート順固定・3大並列構造）

```text
c:/Users/kuseg/lab/16_cxt_db/
├── AGENTS.md                  # スキーマ層：エージェント用運用プロトコル規約書
├── README.md                  # 人間用ガイド：Obsidian連携・運用マニュアル
├── index.md                   # カタログ：主観・客観の全索引と1行要約
├── log.md                     # 監査ログ：時系列作業記録
├── .gitignore                 # Git除外設定
│
├── 05-raw/                    # 【生データ層：不変の唯一の入口】
│   ├── mishori/               # 蒸留待ち（記事、壁打ちメモ、対話ログ何でもここへ）
│   ├── shorizumi/             # 蒸留完了済みの生データ保管庫
│   └── sozai/                 # 記事付属の画像・図版素材
│
├── 10-syukan/                 # 【主観層：じぶん取説・お作法・ダメ出し記憶】
│   ├── kihon-houshin.md       # 全ドメイン共通の根本哲学・判断軸マスター
│   ├── html-css/              # ドメイン：HTML/CSS
│   │   ├── rule.md            # 確定お作法・推奨コード見本
│   │   └── kioku.md           # 指摘履歴・NGパターン記憶
│   └── email/                 # ドメイン：メール
│       ├── rule.md            # 敬語トーン・推奨文面
│       └── kioku.md           # 過去のダメ出し・嫌いな表現記憶
│
├── 15-kyakkan/                # 【客観層：世の中の事実・教科書・技術資料】
│   ├── shiryo/                # 個別資料・ソース要約ノート
│   ├── koyu-meishi/           # 固有名詞ノート（人物、ツール、API仕様）
│   ├── gainen/                # 概念ノート（理論、アーキテクチャ）
│   └── kousatsu/              # 複数資料横断の比較・総括レポート
│
├── docs/                      # ガイド・メモ
└── scripts/                   # CLI支援ユーティリティ
    └── wiki_cli.py
```

---

## 💡 コア運用の仕組み

1. **生データ入口は1箇所（`05-raw/mishori/`）**:
   - 「これは外の知識？内の知識？」と分類に迷う必要はありません。記事も壁打ちメモもすべて `05-raw/mishori/` に放り込むだけでOKです。
2. **AIが「客観（15）」と「主観（10）」へ自動蒸留**:
   - チャットで `--ingest` と指示するだけで、AIが中身を読み解き：
     - 技術的事実・仕様 ➡ `15-kyakkan/` へ
     - あなたのこだわり・ダメ出し ➡ `10-syukan/<ドメイン>/kioku.md` へ自動分解して整理します。
3. **作業時は最小限のトークンで実行**:
   - HTML作業を依頼されたら、AIは `10-syukan/html-css/rule.md` だけを読んで作業するため、トークン浪費を防ぎます。

---

## 🛠️ CLI ユーティリティ (`scripts/wiki_cli.py`)

```powershell
# 1. 生ソースの取り込み準備（URLやファイルを 05-raw/mishori へ）
python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py --ingest "https://example.com/article"

# 2. Wikiの整合性チェック（リンク切れ、孤立ページ検出）
python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py lint

# 3. ナレッジベースの統計情報表示（ドメイン数、ページ数、リンク密度）
python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py stats

# 4. キーワード検索
python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py search "Karpathy"
```
