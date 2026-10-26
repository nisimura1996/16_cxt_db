# 知識カタログ (index.md)

本ファイルは、Wiki内に蓄積された全ページの一覧および1行要約です。
エージェントは問い合わせ（Query）を受けた際、まずこのファイルを読み込んで関連ページを特定します。

最終更新日: 2026-10-26

---

## 📚 ソース要約 (sources/)
一次情報の要約および抽出メモ。

- [[karpathy-llm-wiki]]: Andrej Karpathy氏によるLLM Wiki提唱Gistの要約。RAGからコンパイル型への移行思想。

---

## 👤 エンティティ (entities/)
人物、組織、プロジェクト、主要ツールなどの固有名詞。

- [[andrej-karpathy]]: AI研究者・教育者。元Tesla AIディレクター、元OpenAI創設メンバー。LLM Wikiの提唱者。

---

## 💡 概念・理論 (concepts/)
手法、理論、設計思想、アーキテクチャパターン。

- [[llm-wiki]]: LLMがMarkdown知識ベースを自律的にコンパイル・維持する永続的ナレッジベース構築手法。
- [[compounding-knowledge]]: 知識が蓄積されるほど相互連関が深まり、価値が幾何級数的に高まる複利型ナレッジの思想。
- [[three-layer-architecture]]: 生ソース層（不変）、Wiki層（LLM管理）、スキーマ層（規約）からなるLLM Wikiの基盤構造。

---

## 🔬 総合考察・比較分析 (synthesis/)
複数ソースを横断して作成された深い洞察や比較レポート。

- [[llm-wiki-vs-rag]]: 従来型RAG（検索型）とLLM Wiki（コンパイル型）のアーキテクチャ・運用思想の徹底比較。
