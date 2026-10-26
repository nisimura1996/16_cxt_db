---
type: concept
title: Compounding Knowledge (複利型知識蓄積)
last_updated: 2026-10-26
sources:
  - "[[sources/karpathy-llm-wiki]]"
tags: [knowledge-management, compounding, learning]
---

# Compounding Knowledge (複利型知識蓄積)

## 定義・概要
**Compounding Knowledge（複利型知識蓄積）** とは、新しい情報を取り込むたびに過去の知識と有機的に結びつき、単なる足し算（線形蓄積）ではなく「掛け算（幾何級数的成長）」で知識ネットワーク全体の価値が高まっていく現象・設計思想を指す。

[[andrej-karpathy|Andrej Karpathy]] 氏は、従来のRAGが「質問のたびにゼロから関連チャンクを探し出すだけの単利（あるいはゼロリセット）システム」であるのに対し、[[llm-wiki|LLM Wiki]] を「永続的・複利型アーティファクト（Persistent Compounding Artifact）」と位置づけた。

## 複利化が起きる条件
1. **事前統合（Pre-compilation）**:
   - 入ってきた知識が独立したファイルとして孤立せず、既存のエンティティや概念ページにその場で統合される。
2. **クロスリファレンス網（Mesh of Wikilinks）**:
   - 関連する概念や人物へのリンク（`[[ページ名]]`）が張り巡らされ、1つのページを起点に関連概念群が芋づる式に想起可能になる。
3. **成果の還元（Writing Back to Wiki）**:
   - ユーザーが深い洞察を求めたり比較分析を行った際、その出力（合成結果）がチャットのタイムラインで消えるのではなく、Wikiの恒久ページ（`synthesis/`）として再保存される。
4. **矛盾・変遷の可視化（Tracking Evolution）**:
   - 古い説と新しい説の衝突を消去せず、「2024年の見解」と「2026年の新事実」として構造化して記録することで、知見の深化の歴史が資産となる。

## 関連ページ
- 中心概念: [[llm-wiki]]
- 提唱者: [[andrej-karpathy]]
- 構造: [[three-layer-architecture]]
- 比較: [[llm-wiki-vs-rag]]
