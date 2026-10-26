#!/usr/bin/env python3
"""
LLM Wiki CLI Utility
Andrej Karpathy提唱のLLM Wiki運用を支援するコマンドラインツール。
- lint: リンク切れ、孤立ページ、index未登録ページの検出
- stats: ナレッジベースの統計情報表示（ページ数、リンク密度）
- search: 全文キーワード検索
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, Set, List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent

# Windows cp932 環境対応
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Wiki管理対象ディレクトリ（日本語ローマ字）
WIKI_DIRS = ["shiryo", "koyu-meishi", "gainen", "kousatsu"]

def get_all_wiki_files() -> Dict[str, Path]:
    """すべてのWiki層Markdownファイルを {stem: Path} で取得"""
    files = {}
    for d in WIKI_DIRS:
        dir_path = ROOT_DIR / d
        if dir_path.is_dir():
            for p in dir_path.glob("*.md"):
                files[p.stem] = p
    return files

def extract_wikilinks(file_path: Path) -> Set[str]:
    """ファイル内の [[target]] または [[target|alias]] を抽出（コードブロックやインラインコード内は除外）"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return set()

    # フェンスされたコードブロック (```...```) を除去
    content = re.sub(r"```[\s\S]*?```", "", content)
    # インラインコード (`...`) を除去
    content = re.sub(r"`[^`\n]+`", "", content)

    # [[target]] または [[target|display]]
    pattern = r"\[\[([a-zA-Z0-9_\-\./]+?)(?:\|.*?)?\]\]"
    matches = re.findall(pattern, content)
    targets = set()
    for m in matches:
        stem = Path(m).stem
        targets.add(stem)
    return targets

def cmd_lint(args):
    """Wiki全体の健全性チェック（Lint）"""
    print("=" * 60)
    print("🔍 LLM Wiki Lint (整合性・健全性チェック)")
    print("=" * 60)

    wiki_files = get_all_wiki_files()
    index_file = ROOT_DIR / "index.md"
    
    # 1. リンク切れチェック & リンクグラフ構築
    inbound_links: Dict[str, Set[str]] = {stem: set() for stem in wiki_files}
    broken_links: List[Tuple[str, str]] = [] # (source_file, missing_target)

    all_scanned_files = list(wiki_files.values())
    if index_file.exists():
        all_scanned_files.append(index_file)

    for p in all_scanned_files:
        source_stem = p.stem
        links = extract_wikilinks(p)
        for target in links:
            if target in wiki_files:
                if source_stem in inbound_links:
                    inbound_links[target].add(source_stem)
            else:
                # 特殊ファイル（index, log, README等）は除外
                if target not in ["index", "log", "README", "AGENTS"]:
                    broken_links.append((str(p.relative_to(ROOT_DIR)), target))

    # 2. 孤立ページ（Orphan Pages）
    orphan_pages = [stem for stem, sources in inbound_links.items() if len(sources) == 0]

    # 3. index.md 未登録ページ
    index_missing = []
    if index_file.exists():
        index_content = index_file.read_text(encoding="utf-8")
        for stem in wiki_files:
            if f"[[{stem}]]" not in index_content and f"[[{stem}|" not in index_content:
                index_missing.append(stem)

    # 結果表示
    has_issues = False

    if broken_links:
        has_issues = True
        print(f"\n❌ リンク切れ (Broken Links): {len(broken_links)} 件")
        for src, target in broken_links:
            print(f"  - {src} -> [[{target}]] (ファイルが存在しません)")
    else:
        print("\n✅ リンク切れはありません。")

    if orphan_pages:
        has_issues = True
        print(f"\n⚠️ 孤立ページ (Orphan Pages - 他のページからの被リンクなし): {len(orphan_pages)} 件")
        for stem in orphan_pages:
            rel_path = wiki_files[stem].relative_to(ROOT_DIR)
            print(f"  - {rel_path}")
    else:
        print("✅ 孤立ページはありません。すべてのページが相互接続されています。")

    if index_missing:
        has_issues = True
        print(f"\n⚠️ index.md 未登録ページ: {len(index_missing)} 件")
        for stem in index_missing:
            print(f"  - [[{stem}]]")
    else:
        print("✅ すべてのWikiページが index.md に登録されています。")

    print("\n" + "=" * 60)
    if not has_issues:
        print("🎉 総合診断: Wikiは完全に健全です！")
    else:
        print("💡 対処法: エージェントに「Lint結果をもとにリンク切れと孤立ページを修正して」と指示してください。")
    print("=" * 60)

def cmd_stats(args):
    """Wiki統計情報の表示"""
    print("=" * 60)
    print("📊 LLM Wiki 統計情報 (Knowledge Base Stats)")
    print("=" * 60)

    raw_mishori = list((ROOT_DIR / "raw" / "mishori").glob("*.md"))
    raw_shorizumi = list((ROOT_DIR / "raw" / "shorizumi").glob("*.md"))

    counts = {}
    total_pages = 0
    wiki_files = get_all_wiki_files()

    for d in WIKI_DIRS:
        dir_path = ROOT_DIR / d
        if dir_path.is_dir():
            md_list = list(dir_path.glob("*.md"))
            counts[d] = len(md_list)
            total_pages += len(md_list)
        else:
            counts[d] = 0

    # リンク数の計測
    total_links = 0
    for p in wiki_files.values():
        total_links += len(extract_wikilinks(p))

    avg_links = total_links / total_pages if total_pages > 0 else 0

    print(f"\n[生ソース層 (raw/)]")
    print(f"  - 蒸留待ち (mishori):   {len(raw_mishori):3d} ファイル")
    print(f"  - 蒸留済み (shorizumi): {len(raw_shorizumi):3d} ファイル")

    print(f"\n[Wiki層 (コンパイル済)]")
    for d in WIKI_DIRS:
        print(f"  - {d:12s}:          {counts[d]:3d} ページ")
    print(f"  ---------------------------------")
    print(f"  - 合計Wikiページ数:     {total_pages:3d} ページ")

    print(f"\n[ネットワーク・接続密度]")
    print(f"  - 総内部リンク数:       {total_links:3d} 本")
    print(f"  - ページ平均リンク数:   {avg_links:.2f} 本/ページ")
    print("=" * 60)

def cmd_search(args):
    """Markdown全文キーワード検索"""
    query = args.query.lower()
    print(f"🔎 検索キーワード: '{args.query}'\n")

    wiki_files = get_all_wiki_files()
    wiki_files["index"] = ROOT_DIR / "index.md"
    wiki_files["AGENTS"] = ROOT_DIR / "AGENTS.md"

    found_count = 0
    for stem, path in wiki_files.items():
        if not path.exists():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue

        matched_lines = []
        for idx, line in enumerate(lines, start=1):
            if query in line.lower():
                matched_lines.append((idx, line.strip()))

        if matched_lines:
            found_count += 1
            rel_path = path.relative_to(ROOT_DIR)
            print(f"📄 {rel_path} ({len(matched_lines)} 件の一致):")
            for idx, snippet in matched_lines[:5]:
                print(f"   L{idx}: {snippet}")
            if len(matched_lines) > 5:
                print(f"   ... 他 {len(matched_lines) - 5} 行")
            print()

    if found_count == 0:
        print("一致するページは見つかりませんでした。")
    else:
        print(f"合計 {found_count} 個のファイルで一致しました。")

def cmd_ingest(target: str = None):
    """生ソースを raw/mishori/ に配置し、Ingestの準備を行う"""
    print("=" * 60)
    print("📥 LLM Wiki Ingest (生ソースの取り込み準備)")
    print("=" * 60)

    mishori_dir = ROOT_DIR / "raw" / "mishori"
    mishori_dir.mkdir(parents=True, exist_ok=True)

    if target:
        # 1. URLの場合
        if target.startswith("http://") or target.startswith("https://"):
            import urllib.request
            import urllib.parse
            from datetime import datetime
            
            print(f"🌐 URLを取得中: {target}")
            try:
                req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req) as res:
                    html = res.read().decode("utf-8", errors="replace")
                
                # タイトル抽出
                title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
                title = title_match.group(1).strip() if title_match else "web-source"
                slug = re.sub(r"[^\w\-_]+", "-", title.lower()).strip("-")[:40] or "source"
                filename = f"{datetime.now().strftime('%Y%m%d')}_{slug}.md"
                dest_file = mishori_dir / filename
                
                # 本文保存
                dest_file.write_text(f"---\nsource_url: {target}\ndate: {datetime.now().strftime('%Y-%m-%d')}\n---\n\n{html}", encoding="utf-8")
                print(f"✅ Webソースを保存しました: {dest_file.relative_to(ROOT_DIR)}")
            except Exception as e:
                print(f"❌ URL取得エラー: {e}")
                return

        # 2. ローカルファイルの場合
        elif Path(target).exists():
            src_path = Path(target)
            dest_file = mishori_dir / src_path.name
            try:
                dest_file.write_bytes(src_path.read_bytes())
                print(f"✅ ファイルを mishori にコピーしました: {dest_file.relative_to(ROOT_DIR)}")
            except Exception as e:
                print(f"❌ ファイルコピーエラー: {e}")
                return
        else:
            # 3. 直接テキストとして扱う場合
            from datetime import datetime
            filename = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            dest_file = mishori_dir / filename
            dest_file.write_text(target, encoding="utf-8")
            print(f"✅ 入力テキストを保存しました: {dest_file.relative_to(ROOT_DIR)}")

    # mishori 内の待機中ファイルを確認
    mishori_files = [f for f in mishori_dir.glob("*") if f.name != ".gitkeep"]
    print(f"\n📂 現在 raw/mishori/ に待機中のソース: {len(mishori_files)} 件")
    for f in mishori_files:
        print(f"  - {f.name}")

    print("\n" + "=" * 60)
    print("🤖 次のステップ:")
    print("AIエージェントに以下の指示を送ると、Wikiへの蒸留・統合が自動実行されます：")
    print(f"👉 「--ingest」 または 「raw/mishori 内のファイルをWikiに取り込んで」")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="LLM Wiki CLI")
    parser.add_argument("--ingest", nargs="?", const="", default=None, help="生ソース（URL、ファイルパス、テキスト）を取り込み準備")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("lint", help="Wiki全体の整合性・リンク切れチェック")
    subparsers.add_parser("stats", help="Wikiの統計情報を表示")

    ingest_parser = subparsers.add_parser("ingest", help="生ソースを取り込み準備")
    ingest_parser.add_argument("target", nargs="?", default=None, help="対象のファイルパス、URL、またはテキスト")

    search_parser = subparsers.add_parser("search", help="キーワード検索")
    search_parser.add_argument("query", help="検索キーワード")

    args = parser.parse_args()

    # --ingest フラグが指定された場合
    if args.ingest is not None:
        cmd_ingest(args.ingest or None)
        return

    if args.command == "lint":
        cmd_lint(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "ingest":
        cmd_ingest(args.target)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
