---
type: synthesis
title: LLM Wiki vs 従来型RAG：知識管理パラダイムの徹底比較
last_updated: 2026-10-26
sources:
  - "[[sources/karpathy-llm-wiki]]"
tags: [synthesis, rag, llm-wiki, architecture-comparison]
---

# LLM Wiki vs 従来型RAG：知識管理パラダイムの徹底比較

## エグゼクティブサマリー
AIを用いたドキュメント検索・ナレッジベース構築において、主流だった「RAG（Retrieval-Augmented Generation）」と、[[andrej-karpathy|Andrej Karpathy]] 氏が提唱した「[[llm-wiki|LLM Wiki]]」の思想・アーキテクチャ・運用コストを比較分析する。

LLM Wikiの本質は、**「質問時の検索（Runtime Retrieval）」から「取り込み時の事前コンパイル（Ahead-of-Time Compilation）」への転換**である。

---

## 比較表

| 比較軸 | 従来型 RAG | Karpathy提唱 LLM Wiki |
| :--- | :--- | :--- |
| **パラダイム** | インデックス型検索（Search & Retrieve） | **知識の事前コンパイル（Compile & Link）** |
| **知識の表現** | ベクトル埋め込み + 生テキストチャンク | **構造化Markdown + 双方向リンク（Wiki）** |
| **処理タイミング** | 質問時に毎回オンデマンドで探索・集約 | **ソース投入時に即時要約・概念抽出・統合** |
| **横断的質問への耐性** | 5文書を跨ぐ複雑な問いではチャンク欠損・文脈分断が多発 | **事前に相互参照されているため高精度に統合回答可能** |
| **矛盾への対応** | 過去データと最新データが混ざりハルシネーションの元凶に | **Ingest時にエージェントが矛盾を検出し併記・対比** |
| **ストレージ可読性** | ベクトルDB（人間にはブラックボックス） | **プレーンテキストMarkdown（GitやObsidianで可視化）** |
| **成長性** | 単利（蓄積しても検索空間が広がるだけで質は上がらない） | **[[compounding-knowledge|複利型]]（ソースが増えるほど知識グラフが濃密化）** |
| **主なツール** | LangChain, LlamaIndex, Pinecone, Chroma | **Obsidian, Git, LLM Agent（Codex, Claude, Gemini）** |

---

## なぜLLM Wikiが優れているのか

### 1. 「毎回ゼロから考え直す」無駄の排除
従来のRAGは、ユーザーが高度な質問をするたびに「関連しそうな断片」をかき集め、コンテキストウィンドウ内で即席のパズルを解かせます。
LLM Wikiでは、ソースを読んだ時点で「この人物が何者か」「この概念がどの技術と関連しているか」が既にWikiページとして整理済みです。LLMはコンパイル済みの知識カタログ（`index.md`）を見て、必要なWikiページだけを直接読むため、思考の深さと一貫性が圧倒的に高くなります。

### 2. ポータビリティとベンダーロックインの排除
RAGを構築すると、特定のベクトルデータベース、エンベディングモデル、チャンキング戦略のコードベースに縛られます。モデルを更新すると全ベクトルの再計算が必要になります。
一方、LLM Wikiの実体は**シンプルなMarkdownフォルダ**です。50年後でも読めるオープンな形式であり、エディタもObsidian、VSCode、端末のcatコマンドまで自由自在です。

### 3. エージェントの自律維持によるエントロピー克服
「Wikiは放置すると腐る」という歴史的課題を、LLMエージェントが専任の司書・保守員として振る舞うことで解決しています。

---

## 関連ページ
- 提唱者: [[andrej-karpathy]]
- 原典ソース: [[sources/karpathy-llm-wiki]]
- コア概念: [[llm-wiki]], [[compounding-knowledge]], [[three-layer-architecture]]
