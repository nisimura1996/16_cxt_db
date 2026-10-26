---
type: concept
title: Three-Layer Architecture (LLM Wikiの3層構造)
last_updated: 2026-10-26
sources:
  - "[[sources/karpathy-llm-wiki]]"
tags: [architecture, design-pattern, llm-wiki]
---

# Three-Layer Architecture (LLM Wikiの3層構造)

## 定義・概要
[[andrej-karpathy|Andrej Karpathy]] 氏が提示した、人間とLLMが安全かつ破綻なくナレッジベースを共同運用するためのシステムアーキテクチャ。責務と権限を明確に分けた3つのレイヤーから構成される。

```text
+-------------------------------------------------------+
| 3. スキーマ層 (The Schema)                            |
|    - AGENTS.md / CLAUDE.md                            |
|    - エージェントの行動憲法・命名規約・運用プロトコル  |
+-------------------------------------------------------+
                           | 指針
                           v
+-------------------------------------------------------+
| 2. Wiki層 (The Wiki)                                  |
|    - sources/, entities/, concepts/, synthesis/       |
|    - index.md, log.md                                 |
|    - LLMが100%管理・編集・維持するMarkdown知識グラフ   |
+-------------------------------------------------------+
                           ^ 抽出・蒸留
                           | (不変参照)
+-------------------------------------------------------+
| 1. 生ソース層 (Raw Sources)                           |
|    - raw/pending/, raw/ingested/, raw/assets/         |
|    - 人間が集めた一次情報（記事、論文、議事録、画像）  |
|    - 不変（Immutable：LLMは書き換えない）            |
+-------------------------------------------------------+
```

## 各層の詳細と運用原則

### 1. 生ソース層 (Raw Sources)
- **保管場所**: `raw/pending/`（未処理）、`raw/ingested/`（処理済）、`raw/assets/`（添付メディア）
- **特性**: **不変（Immutable）**。ソースオブトゥルース（信頼できる唯一の情報源）として永久保存される。
- **原則**: LLMは内容を読み取ってWiki層へ抽出するが、元ファイル自体を書き換えてはならない。

### 2. Wiki層 (The Wiki)
- **保管場所**: `sources/`, `entities/`, `concepts/`, `synthesis/`, `index.md`, `log.md`
- **特性**: **可変・成長型（Mutable & Compounding）**。
- **原則**: 人間は原則として手動編集せず、LLMが編集・更新・リンク張りを一手に引き受ける。

### 3. スキーマ層 (The Schema)
- **保管場所**: `AGENTS.md`
- **特性**: **メタ指示（Meta Configuration）**。
- **原則**: エージェントを単なるおしゃべりボットから「厳格で几帳面なWiki編纂者」へと変貌させるためのルールセット。

## 関連ページ
- 中心概念: [[llm-wiki]]
- 提唱者: [[andrej-karpathy]]
- 運用効果: [[compounding-knowledge]]
- 比較分析: [[llm-wiki-vs-rag]]
