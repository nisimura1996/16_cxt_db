---
type: syukan-rule
domain: html-css
title: HTML/CSS お作法・確定ルール
last_updated: 2026-10-26
tags: [html, css, frontend, rule]
---

# HTML/CSS お作法・確定ルール (rule.md)

AIがHTML/CSS関連のコード作成や編集を行う際に遵守すべき最新の確定ルールです。  
過去の指摘履歴やNGパターンの詳細は [[kioku]] を参照してください。

---

## 1. HTML構造の基本ルール
- **セマンティックタグの優先**:
  - 無意味な `<div>` の多用を避け、`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>` などの意味的タグを正しく使用する。
  - 独立したコンテンツには `<article>`、意味的な区切りには `<section>` を用いる。
- **クラス命名・CSS**:
  - クラス名は役割が明確な命名（BEMライクまたはコンポーネント指向）とする。
  - インラインスタイル（`style="..."`）の乱用は避け、CSSクラスに集約する。

---

## 2. コード見本

### ❌ NGパターン
```html
<div class="box1">
  <div class="box2">タイトル</div>
  <div class="box3">本文テキスト...</div>
</div>
```

### ✅ 推奨パターン
```html
<article class="card">
  <header class="card__header">
    <h2 class="card__title">タイトル</h2>
  </header>
  <div class="card__body">
    <p>本文テキスト...</p>
  </div>
</article>
```
