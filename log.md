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
