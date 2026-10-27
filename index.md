# 知識カタログ (index.md)

本ファイルは、Wiki内に蓄積された全ページの一覧および1行要約です。
エージェントは問い合わせや作業依頼を受けた際、まずこのファイルを読み込んで必要なドメイン・知識ページを特定します。

最終更新日: 2026-10-27

---

## 🧭 主観層・じぶん取説 (10-syukan/)
あなたの好み・美意識・確定ルール・ダメ出し履歴の蓄積。

- [[10-syukan/kihon-houshin|kihon-houshin]]: 全ドメイン共通の根本哲学・外部記憶化と再説明ゼロ、スキル集約・頭脳と手足の分離。
- **html-css/**:
  - [[10-syukan/html-css/rule|html-css/rule]]: HTML/CSSの確定お作法（セマンティックタグ優先、BEM命名、コード見本）。
  - [[10-syukan/html-css/kioku|html-css/kioku]]: 過去のダメ出し・指摘履歴（div乱用の禁止など）。
- **email/**:
  - [[10-syukan/email/rule|email/rule]]: メール文面の確定お作法（簡潔明快、自然な丁寧体、過剰敬語の排除、文面見本）。
  - [[10-syukan/email/kioku|email/kioku]]: 過去のダメ出し・指摘履歴（過剰敬語・重厚表現の回避など）。

---

## 📚 客観層・教科書 (15-kyakkan/)
世の中の普遍的な知識・一次資料・アーキテクチャ。

### 資料・要約 (shiryo/)
- [[karpathy-llm-wiki]]: Andrej Karpathy氏によるLLM Wiki提唱Gistの要約。RAGからコンパイル型への移行思想。

### 固有名詞 (koyu-meishi/)
- [[andrej-karpathy]]: AI研究者・教育者。元Tesla AIディレクター、元OpenAI創設メンバー。LLM Wikiの提唱者。

### 概念・理論 (gainen/)
- [[llm-wiki]]: LLMがMarkdown知識ベースを自律的にコンパイル・維持する永続的ナレッジベース構築手法。
- [[compounding-knowledge]]: 知識が蓄積されるほど相互連関が深まり、価値が幾何級数的に高まる複利型ナレッジの思想。
- [[three-layer-architecture]]: 生データ層（不変）、Wiki層（LLM管理）、スキーマ層（規約）からなるLLM Wikiの基盤構造。
- [[external-memory-and-tool-separation]]: 外部記憶による再説明ゼロ化と、頭脳（スキル）と手足（Pythonスクリプト）の責務分離設計思想。

### 考察・まとめ (kousatsu/)
- [[llm-wiki-vs-rag]]: 従来型RAG（検索型）とLLM Wiki（コンパイル型）のアーキテクチャ・運用思想の徹底比較。
