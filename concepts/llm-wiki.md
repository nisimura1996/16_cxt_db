---
type: concept
title: LLM Wiki
last_updated: 2026-10-26
sources:
  - "[[sources/karpathy-llm-wiki]]"
tags: [knowledge-base, architecture, ai-agent, obsidian]
---

# LLM Wiki

## 定義・概要
**LLM Wiki** とは、[[andrej-karpathy|Andrej Karpathy]] 氏が提唱した個人・チーム向けの永続的ナレッジベース構築パターンである。

従来の都度検索型RAG（Retrieval-Augmented Generation）とは異なり、情報源が追加されるたびにAIエージェントがMarkdownファイル群（Wiki）を「事前コンパイル」し、要約、エンティティ抽出、概念整理、相互リンク付け、過去記述との矛盾解消を自律的に行いながら永続的に成長させる仕組みを指す。

## なぜ機能するのか（コアメカニズム）
ナレッジベースが破綻・放置される最大の原因は「維持管理コスト（メンテナンス負担）のエントロピー増大」にある。
- 人間は新しい記事を読んでも、過去の数十ページにわたる関連メモを開いて相互リンクを張り直したり、主張の食い違いを記録する作業を継続できない。
- 一方、LLMは疲れを知らず、1つの新情報から10〜15の関連ファイルを瞬時に特定して更新できる。
- **「人間はインプット・問いかけ・キュレーションに専念し、LLMがメンテナンス作業を100%担う」** ことで、持続可能な知識資産が形成される。

## 主要な構成要素
1. **[[three-layer-architecture|3層アーキテクチャ]]**:
   - `raw/`（生ソース層） / Wiki層（Markdown群） / スキーマ層（`AGENTS.md`）
2. **コアオペレーション**:
   - Ingest（取り込み・蒸留・統合）
   - Query & Synthesis（横断検索・統合回答・Wikiへの還元）
   - Lint（定期健康診断・矛盾検出・孤立ページ解消）
3. **ナビゲーションと監査**:
   - `index.md`: コンテンツ指向カタログ（LLMが真っ先に読む）
   - `log.md`: 時系列監査ログ（CLIツールで容易にパース可能）

## 関連ページ
- 提唱者: [[andrej-karpathy]]
- ソース: [[sources/karpathy-llm-wiki]]
- 関連概念: [[compounding-knowledge]], [[three-layer-architecture]]
- 比較分析: [[llm-wiki-vs-rag]]
