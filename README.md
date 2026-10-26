# LLM Wiki (16_cxt_db)

Andrej Karpathy（アンドレイ・カルパシー）が提唱した設計思想に基づく、**AIエージェントと人間が協調して育て上げる永続的・複利型のナレッジベース**です。

---

## 💡 コア思想：RAGから「知識のコンパイル」へ

| 比較項目 | 従来型 RAG (Retrieval-Augmented Generation) | Karpathy提唱 LLM Wiki |
| :--- | :--- | :--- |
| **知識の保持形態** | 生ドキュメント（PDF/テキスト）のチャンク断片 | **相互リンクされたMarkdownのWiki構造** |
| **処理タイミング** | 質問されるたびに毎回ゼロから検索・抽出 | **ソース追加時に即座にコンパイル・統合・蓄積** |
| **知識の成長** | 蓄積されない（毎回ゼロスタート） | **複利（Compounding）的に深まり繋がる** |
| **矛盾・変化** | 矛盾する情報がそのまま混在してノイズ化 | **エージェントが矛盾・変遷を検出し対比整理** |
| **人間の役割** | 検索キーワードの工夫、ノイズの仕分け | **情報源のキュレーション、探求、本質的な問い** |
| **AIの役割** | その場限りの回答生成 | **Wiki全体の専任メンテナンス・編纂者** |

> 「Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.」  
> （ObsidianがIDEであり、LLMがプログラマーであり、Wikiがコードベースである）  
> — Andrej Karpathy

---

## 📂 ディレクトリ構成

- `raw/` : 一次情報（不変のソースオブトゥルース）
  - `mishori/` : 未処理の生ドキュメント（Web記事クリップ、論文、メモ等）
  - `shorizumi/` : Wikiへ統合済みの生ドキュメント
  - `sozai/` : 添付画像・図版・素材
- `shiryo/` : 元データごとの個別要約・抽出ノート
- `koyu-meishi/` : 固有名詞ページ（人物、組織、プロダクト、ツール）
- `gainen/` : 概念ページ（理論、設計パターン、手法）
- `kousatsu/` : 複数資料横断の比較・総括レポート
- `scripts/` : Wikiの自動診断・統計・管理スクリプト
- `index.md` : 全ページのカタログと1行要約（LLMが真っ先に参照する索引）
- `log.md` : 時系列の作業・監査ログ
- `AGENTS.md` : AIエージェント用の運用プロトコル規約書

---

## 🖥️ おすすめの運用環境 (Obsidian連携)

本ディレクトリ（`c:/Users/kuseg/lab/16_cxt_db`）は、**Obsidian**のVault（保管庫）としてそのまま開くことができます。

1. **Obsidian**を開き、「Open folder as vault（フォルダを保管庫として開く）」を選択。
2. 本フォルダ（`16_cxt_db`）を指定。
3. エージェントがリアルタイムで作成・更新するWikiページや、`Graph View`（知識グラフ）、双方向リンクをビジュアルに閲覧・探索できます。

---

## 🛠️ CLI ユーティリティ (`scripts/wiki_cli.py`)

本ワークスペースには、整合性チェックや統計確認のためのPythonツールが標準配備されています。

```powershell
# 1. 生ソースの取り込み準備（URLやファイルを pending へ）
python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py --ingest "https://example.com/article"

# 2. Wikiの整合性チェック（リンク切れ、孤立ページ、空参照の検出）
python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py lint

# 3. ナレッジベースの統計情報表示（ページ数、リンク密度、カテゴリ内訳）
python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py stats

# 4. Wiki内キーワード検索
python C:\Users\kuseg\lab\16_cxt_db\scripts\wiki_cli.py search "Karpathy"
```

---

## 🚀 運用フロー

1. **新しいソースを取り込むとき (Ingest)**:
   - 「`--ingest`」とチャットで打つか、「`raw/mishori/` に置いたファイルをWikiに取り込んで」と指示。
2. **調べ物・質問をするとき (Query)**:
   - 「Wiki内の知識をもとに〇〇について教えて」「AとBの違いを比較して」と質問。
   - 有用な回答は自動的に `kousatsu/` ページとしてWikiに還元されます。
3. **定期的なメンテナンス (Lint)**:
   - 「Wikiの健康診断（Lint）をして」と依頼すると、エージェントが矛盾・孤立ページ・リンク切れを解消します。
