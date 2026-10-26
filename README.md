# LLM Wiki (16_cxt_db)

Andrej Karpathy（アンドレイ・カルパシー）が提唱した設計思想に基づき、**「客観的知識（世の中の事実）」**と**「主観的知識（じぶん取説・お作法）」**を同一ワークスペースで共存・運用する永続的ナレッジベースです。

---

## 📂 ディレクトリ構成（ソート順固定・3大並列構造）

```text
c:/Users/kuseg/lab/16_cxt_db/
├── AGENTS.md                  # スキーマ層：エージェント用運用プロトコル規約書（35行）
├── README.md                  # 人間用ガイド：Obsidian連携・運用マニュアル（本ファイル）
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
├── docs/                      # ユーザー固有メモ
└── scripts/                   # CLI支援ユーティリティ
    └── wiki_cli.py
```

---

## 💡 コア運用の仕組み

1. **生データ入口は1箇所（`05-raw/mishori/`）**:
   - 「外の知識？内の知識？」と分類に迷う必要はありません。記事も壁打ちメモもすべて `05-raw/mishori/` に放り込むだけでOKです。
2. **AIが「客観（15）」と「主観（10）」へ自動蒸留**:
   - チャットで `--ingest` と指示するだけで、AIが中身を読み解き：
     - 技術的事実・仕様 ➡ `15-kyakkan/` 配下の該当フォルダへ
     - あなたのこだわり・ダメ出し ➡ `10-syukan/<ドメイン>/kioku.md` へ自動分解して整理します。
3. **作業時は最小限のトークンで実行（Single Source of Truth）**:
   - 作業時、AIは該当ドメインの `10-syukan/<ドメイン>/rule.md` だけを読んで作業するため、トークン浪費を防ぎます。
   - ルールや規約は複数箇所に書かず、該当ファイル1箇所のみに集約してメンテナンス性を維持します。

---

## 📖 運用マニュアル（頼み方ガイド）

### 1. 生データの取り込みと自動蒸留 (Ingest)

記事、論文、対話ログ、メモなど、すべての生データは `05-raw/mishori/` に集約されます。

- **💬 自然言語・短縮コマンドでの頼み方**:
  - 短縮コマンド（最速）:
    - `--ingest`（05-raw/mishori/ 内の待機ファイルを一括取り込み）
    - `--ingest https://example.com/article`
    - `--ingest 05-raw/mishori/memo.md`
  - URLから直接取り込む:
    - 「このWeb記事をWikiに取り込んで：https://example.com/article」
  - 壁打ちメモ・ダメ出しを直接渡す:
    - 「以下の会話ログから、技術仕様は客観へ、私のダメ出しは主観のhtml-cssドメインへ反映して：（テキスト貼り付け）」
  - 置いたファイルを処理させる:
    - 「05-raw/mishori/ に置いた memo.md をWikiに取り込んで、完了したら shorizumi/ に移して」

- **💻 コード・CLIでの頼み方**:
  ```powershell
  # 1. CLIからワンライナーで取り込み準備（05-raw/mishoriへ配置）
  python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py --ingest "https://example.com/article"
  python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py --ingest "C:\path\to\file.md"

  # 2. 引数なしで mishori の待機状況を確認
  python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py --ingest
  ```

---

### 2. 蓄積知識の検索・質問・作業生成 (Query & Generation)

作業依頼を受けた際、AIは最小限のトークン（該当ドメインのお作法 `rule.md` のみ）を読み込んで回答・コード生成します。

- **💬 自然言語での頼み方**:
  - ドメインお作法を守った成果物作成:
    - 「html-cssのお作法を守って、プロフィールカードのHTML/CSSを作成して」
  - 客観Wiki横断の質問:
    - 「15-kyakkan内の知識をもとに、RAGとLLM Wikiの最大の違いを初心者向けに説明して」
  - 成果のWiki還元（最重要）:
    - 「この比較分析の内容を、後から再利用できるように 15-kyakkan/kousatsu/ フォルダに新しいページとして保存し、index.md にも追加して」
  - 過去のダメ出し・記憶の確認:
    - 「html-cssドメインで過去にどんなダメ出しをしたか一覧で見せて」

- **💻 コード・CLIでの頼み方**:
  ```powershell
  # CLIによるキーワード全文検索
  python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py search "div"
  python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py search "RAG"
  ```

---

### 3. Wikiの整合性チェック・健康診断 (Lint)

Wikiが成長するにつれて発生するリンク切れ、孤立ページ、知識の矛盾、情報の陳腐化を解消します。

- **💬 自然言語での頼み方**:
  - 定期健康診断:
    - 「Wiki全体のLint（整合性チェック）を実行して、リンク切れや孤立ページがあれば直して」
  - 知識の矛盾・古い情報の更新:
    - 「最新のソースと昔のページで主張が食い違っている箇所がないか精査して。見つかったら新旧の比較を併記して」

- **💻 コード・CLIでの頼み方**:
  ```powershell
  # 整合性・リンク切れ・孤立ページの自動診断
  python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py lint

  # 統計情報の表示（ドメイン数、ページ数、リンク密度）
  python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py stats
  ```

---

### 4. 自分の好み・ダメ出しの記録 (Feedback & Rules)

日常の作業でAIに手直しを指示した際、その場で主観層に記録させる操作です。

- **💬 自然言語での頼み方**:
  - ダメ出しの即時記録:
    - 「今言った『メール文面で〜につきましてを多用しない』という指摘を、emailドメインの kioku.md に追記して、rule.md も更新して」
  - 新規ドメインの追加（必ず rule.md と kioku.md がペア作成されます）:
    - 「新たに python ドメインを作って、エラーハンドリングのお作法を登録して」

---

## 🛠️ CLI ユーティリティ早見表 (`scripts/wiki_cli.py`)

| コマンド | 説明 |
| :--- | :--- |
| `python scripts/wiki_cli.py --ingest [URL/パス]` | 生データを `05-raw/mishori/` へ保存・配置 |
| `python scripts/wiki_cli.py lint` | リンク切れ・孤立ページ・未登録ページの自動検出 |
| `python scripts/wiki_cli.py stats` | ドメイン数、ページ数、WikiLink数の統計サマリ表示 |
| `python scripts/wiki_cli.py search "<キーワード>"` | Wiki内の全文検索 |
