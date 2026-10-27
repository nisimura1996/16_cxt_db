# 運用・監査ログ (log.md)

本ファイルは、Wiki内で実行された操作（Ingest / Query / Lint / Init）の時系列追記型ログです。
各エントリのヘッダーは `## [YYYY-MM-DD] <operation> | <title>` 形式で統一されており、CLIツールやスクリプトから容易に解析可能です。

---

## [2026-10-26] init | ワークスペース初期化とLLM Wiki基盤構築
- 種別: 初期セットアップ
- 実行内容:
  - Karpathyの提唱思想に基づき3層構造（`raw/`, Wiki層, `AGENTS.md`）のディレクトリツリーを構築。
  - 人間用ガイド `README.md`、エージェント用規約書 `AGENTS.md`、カタログ `index.md`、Git設定を作成。
  - CLI支援ツール `scripts/wiki_cli.py` を配備。

## [2026-10-26] ingest | Andrej Karpathy: LLM Wiki Idea Gist
- ソース: `raw/ingested/karpathy-llm-wiki.md`
- 出典: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- 作成・更新ファイル:
  - `sources/karpathy-llm-wiki.md` (個別要約)
  - `entities/andrej-karpathy.md` (人物エンティティ)
  - `concepts/llm-wiki.md` (中核概念)
  - `concepts/compounding-knowledge.md` (複利型知識蓄積)
  - `concepts/three-layer-architecture.md` (3層構造)
  - `synthesis/llm-wiki-vs-rag.md` (RAGとの徹底比較レポート)
  - `index.md` (カタログ登録)
- 要約: LLM Wikiの提唱Gistを取り込み、Wikiのブートストラップ（初期知識ベース化）を完了。

## [2026-10-26] refactor | ディレクトリおよびファイル構造の日本語ローマ字化
- 種別: 構造改善・命名変更
- 実行内容:
  - 英語ディレクトリ名を役割が直感的に把握できる日本語ローマ字へ移行：
    - `sources/` ➡ `shiryo/`（資料要約ノート）
    - `entities/` ➡ `koyu-meishi/`（固有名詞・人物・ツール）
    - `concepts/` ➡ `gainen/`（概念・理論・アーキテクチャ）
    - `synthesis/` ➡ `kousatsu/`（複数資料横断の考察レポート）
    - `raw/pending/` ➡ `raw/mishori/`（未処理生データ）
    - `raw/ingested/` ➡ `raw/shorizumi/`（処理済み生データ）
    - `raw/assets/` ➡ `raw/sozai/`（添付画像・素材）
  - 全Markdownファイル内のYAMLフロントマター（`type: shiryo` 等）およびWikiLink、ドキュメント、CLIスクリプト（`wiki_cli.py`）をすべて連動更新。

## [2026-10-26] arch | 3大並列構造（05-raw, 10-syukan, 15-kyakkan）への再編
- 種別: アーキテクチャ強化・ソート順固定
- 実行内容:
  - 認知的負荷ゼロ化のため、生データ入口を `05-raw/mishori/` に完全集約（外も内もここへ投入）。
  - ディレクトリをソート順固定の3大並列構造へ再編：
    - `05-raw/`: 生データ層（不変の唯一の入口）
    - `10-syukan/`: 主観層（じぶん取説・お作法・ダメ出し記憶）
      - `kihon-houshin.md`（共通哲学）
      - `<ドメイン>/rule.md`（確定お作法）と `<ドメイン>/kioku.md`（NG履歴・ダメ出し記憶）
    - `15-kyakkan/`: 客観層（世の中の事実・教科書）
      - `shiryo/`, `koyu-meishi/`, `gainen/`, `kousatsu/` を集約。
  - `wiki_cli.py`、`AGENTS.md`、`index.md`、`README.md`、`docs/` を全面連動更新。

## [2026-10-27] ingest | メール文面・敬語トーン（文体）の自動蒸留
- ソース: `05-raw/shorizumi/2026-10-27_email-buntai.md`
- 反映先:
  - `10-syukan/email/rule.md` (お作法・文面見本更新)
  - `10-syukan/email/kioku.md` (ダメ出し記憶更新)
  - `index.md` (カタログ更新)
- 要約: AIポン出しの過剰・重厚な敬語表現（「〜稼働しております」「〜ございません」「〜直接実施いたします」等）を、自然ですっきりとした丁寧体（「〜稼働しています」「〜ありません」「〜実施します」）へ是正。不要な強調修飾語の排除および箇条書き階層インデント方針を主観層へ蒸留。
