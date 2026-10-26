---
type: shiryo
title: LLM Wiki Idea Gist
author: "[[andrej-karpathy|Andrej Karpathy]]"
source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
torikomi_date: 2026-10-26
tags: [knowledge-base, llm-wiki, rag, obsidian, architecture]
---

# LLM Wiki Idea Gist (Andrej Karpathy)

## 概要
AI研究者の [[andrej-karpathy|Andrej Karpathy]] 氏が公開したGitHub Gist。従来の都度検索型RAG（Retrieval-Augmented Generation）に代わる、AIエージェントを活用した個人・組織向けナレッジベース構築の新パラダイム「[[llm-wiki|LLM Wiki]]」の概念と設計パターンを提示したドキュメント。

## 主要ポイント
1. **RAGの限界とコンパイル型アプローチ**:
   - 従来のRAGは質問のたびに生データをゼロから再探索・再集約するため、知識の永続的な蓄積（[[compounding-knowledge|複利型蓄積]]）が起きない。
   - LLM Wikiは、情報源を追加した時点でLLMがMarkdown Wikiとして事前コンパイルし、常に最新状態に維持する。
2. **[[three-layer-architecture|3層アーキテクチャ]]**:
   - 生ソース層（不変）、Wiki層（LLM管理）、スキーマ層（規約ファイル：`AGENTS.md` / `CLAUDE.md`）。
3. **運用の3大オペレーション**:
   - **Ingest（取り込み）**: 資料の要約、固有名詞/概念の更新、矛盾検出、リンク張り。
   - **Query（問い合わせと還元）**: Wiki横断回答。有益な回答は新たな考察ページとして還元。
   - **Lint（健全性維持）**: 矛盾、陳腐化、孤立ページ、情報ギャップの定期解消。
4. **Obsidianとの親和性**:
   - 「ObsidianがIDE、LLMがプログラマー、Wikiがコードベース」。人間はGUIやGraph Viewで閲覧し、LLMが編集を担当。
5. **Vannevar BushのMemex（1945）の具現化**:
   - 人間が挫折してきた「膨大な相互リンクと整合性メンテナンスの負荷」をLLMが肩代わりすることで、真の連想記憶体系を実現する。

## 抽出した固有名詞 & 概念
- 固有名詞: [[andrej-karpathy]]
- 概念: [[llm-wiki]], [[compounding-knowledge]], [[three-layer-architecture]]
- 考察: [[llm-wiki-vs-rag]]
