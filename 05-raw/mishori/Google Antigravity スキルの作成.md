---
title: "Google Antigravity スキルの作成"
source: "https://codelabs.developers.google.com/getting-started-with-antigravity-skills?hl=ja#0"
author:
  - "[[Google Codelabs]]"
published:
created: 2026-03-19
description: "この Codelab では、専門知識とワークフローを使用して AI エージェントの機能を拡張するための軽量なオープン形式である Antigravity Skills について説明します。このラボでは、複数のエージェント スキルを構築し、Antigravity で使用する方法について説明します。"
tags:
  - "clippings"
---
## Google Antigravity Skills の作成

*access\_time* 残り 77 分Google Antigravity Skills の作成

## この Codelab について

*subject* 最終更新: 2月 11, 2026

*account\_circle* 作成者: Romin Irani

## 1\. はじめに

Google Antigravity は、Google のエージェント型 IDE です。この Codelab では、Antigravity を使用してエージェント スキルを構築します。これは、専門知識とワークフローで AI エージェントの機能を拡張するための軽量のオープン フォーマットです。エージェント スキルとは何か、そのメリット、構築方法について学習します。次に、Git フォーマッタ、テンプレート ジェネレータ、ツールコード スキャフォールディングなど、さまざまなエージェント スキルを構築します。これらはすべて Antigravity 内で使用できます。

**前提条件:**

- Google Antigravity がインストールされ、構成されている。
- Google Antigravity の基本的な理解。Codelab: [**Google Antigravity を使ってみる**](https://codelabs.developers.google.com/getting-started-google-antigravity?hl=ja) を完了することをおすすめします。

## 2\. スキル機能のメリット

最新の AI エージェントは、単純なリスナーから、ローカル ファイル システムや外部ツール（ [MCP サーバー](https://github.com/modelcontextprotocol/servers) 経由）と統合する複雑な推論エンジンへと進化しました。ただし、エージェントにコードベース全体と数百ものツールを無差別に読み込むと、 **コンテキストの飽和** と「ツールの肥大化」が発生します。コンテキスト ウィンドウが大きくても、未使用のツールの 4 ～ 5 万個のトークンをアクティブ メモリにダンプすると、レイテンシの増加、費用の無駄遣い、コンテキストの劣化（モデルが関連性のないデータによって混乱する）が発生します。

## 解決策: エージェントのスキル

この問題を解決するために、Anthropic は [**エージェント スキル**](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) を導入し、アーキテクチャをモノリシック コンテキスト読み込みから **プログレッシブ開示** に移行しました。セッションの開始時に、モデルに特定のワークフロー（データベースの移行やセキュリティ監査など）をすべて「記憶」させるのではなく、これらの機能はモジュール式の検出可能なユニットにパッケージ化されています。

## 仕組み

モデルは、最初はメタデータの軽量な「メニュー」にのみ公開されます。ユーザーのインテントがスキルと明確に一致した場合にのみ、重い手続き型知識（手順とスクリプト）を読み込みます。これにより、認証ミドルウェアのリファクタリングをリクエストしたデベロッパーは、関連のない CSS パイプラインを読み込むことなくセキュリティ コンテキストを取得し、コンテキストを簡潔、高速、費用対効果の高い状態に保つことができます。

![d3f4bcb065a19fea.png](https://codelabs.developers.google.com/static/getting-started-with-antigravity-skills/img/d3f4bcb065a19fea_2880.png?hl=ja)

## 3\. エージェント スキルと Antigravity

Antigravity エコシステムでは、エージェント マネージャーが脳、エディタがキャンバスであるとすると、 **スキル** は、汎用的な Gemini 3 モデルと特定のコンテキストのギャップを埋める専門的なトレーニング モジュールとして機能します。これにより、エージェントは、関連するタスクがリクエストされた場合にのみ、定義された一連の手順とプロトコル（データベース移行標準やセキュリティ チェックなど）を「装備」できます。これらの実行プロトコルを動的に読み込むことで、スキルは AI を汎用的なプログラマーから、組織の成文化されたベスト プラクティスと安全基準を厳格に遵守するスペシャリストへと効果的に変革します。

## Antigravity のスキルとは何ですか？

Google Antigravity のコンテキストでは、スキルは定義ファイル（ `SKILL.md` ）とオプションのサポート アセット（スクリプト、リファレンス、テンプレート）を含むディレクトリ ベースのパッケージです。

これは、オンデマンド機能拡張のメカニズムです。

- **オンデマンド**: システム プロンプト（常に読み込まれる）とは異なり、スキルは、エージェントがユーザーの現在のリクエストに関連すると判断した場合にのみ、エージェントのコンテキストに読み込まれます。これにより、コンテキスト ウィンドウが最適化され、エージェントが無関係な指示に気を取られるのを防ぐことができます。数十個のツールを使用する大規模なプロジェクトでは、この選択的読み込みがパフォーマンスと推論の精度に不可欠です。
- **Capability Extension**: スキルは指示するだけでなく、実行することもできます。Python スクリプトまたは Bash スクリプトをバンドルすることで、スキルはエージェントにローカルマシンまたは外部ネットワークで複雑な複数ステップのアクションを実行する機能を提供できます。ユーザーが手動でコマンドを実行する必要はありません。これにより、エージェントはテキスト ジェネレータからツールユーザーに変わります。

## スキルとエコシステム（ツール、ルール、ワークフロー）

Model Context Protocol（MCP）は、エージェントの「手」として機能し、GitHub や PostgreSQL などの外部システムへのヘビーデューティで永続的な接続を提供しますが、スキルはそれらを指示する「脳」として機能します。

MCP はステートフル インフラストラクチャを処理しますが、スキルはこれらのツールの使用方法をパッケージ化した軽量で一時的なタスク定義です。このサーバーレス アプローチにより、エージェントは永続的なプロセスの実行に伴う運用上のオーバーヘッドなしで、アドホック タスク（変更ログや移行の生成など）を実行できます。タスクがアクティブな場合にのみコンテキストを読み込み、タスクの完了直後にコンテキストを解放します。

機能面では、スキルは「ルール」（受動的で常に有効なガードレール）と「ワークフロー」（能動的でユーザーがトリガーするマクロ）の中間的な位置を占めています。特定のコマンド（ `/test` など）を必要とするワークフローとは異なり、スキルは **エージェントによってトリガー** されます。モデルはユーザーの意図を自動的に検出し、必要な特定の専門知識を動的に提供します。このアーキテクチャにより、強力なコンポーザビリティが可能になります。たとえば、グローバル ルールでデータベースの変更時に「Safe-Migration」スキルを使用するように強制したり、単一のワークフローで複数のスキルをオーケストレートして堅牢なデプロイ パイプラインを構築したりできます。

## 4\. スキルを作成する

Antigravity でスキルを作成するには、特定のディレクトリ構造とファイル形式に従う必要があります。この標準化により、スキルがポータブルになり、エージェントがスキルを確実に解析して実行できるようになります。この設計は意図的にシンプルになっており、マークダウンや YAML などの広く理解されている形式に依存しているため、IDE の機能を拡張したいデベロッパーにとっての参入障壁が低くなっています。

## ディレクトリ構造

スキルは 2 つのスコープで定義できるため、プロジェクト固有のカスタマイズとユーザー固有のカスタマイズの両方が可能です。

1. **Workspace Scope**: `<workspace-root>/.agent/skills/` にあります。これらのスキルは、特定のプロジェクト内でのみ使用できます。これは、特定の環境へのデプロイ、アプリのデータベース管理、独自のフレームワークのボイラープレート コードの生成など、プロジェクト固有のスクリプトに最適です。
2. **グローバル スコープ**: `~/.gemini/antigravity/skills/` にあります。これらのスキルは、ユーザーのマシンのすべてのプロジェクトで使用できます。これは、「JSON のフォーマット」、「UUID の生成」、「コードスタイルのレビュー」などの一般的なユーティリティや、個人の生産性向上ツールとの統合に適しています。

一般的な Skill ディレクトリは次のようになります。

```
my-skill/
├── SKILL.md # The definition file
├── scripts/ # [Optional] Python, Bash, or Node scripts
     ├── run.py
     └── util.sh
├── references/ # [Optional] Documentation or templates
     └── api-docs.md
└── assets/ # [Optional] Static assets (images, logos)
```

この構造により、関心を効果的に分離できます。ロジック（ `scripts` ）は、指示（ `SKILL.md` ）と知識（ `references` ）から分離されており、標準的なソフトウェア エンジニアリング プラクティスを反映しています。

### SKILL.md 定義ファイル

SKILL.md ファイルはスキルの頭脳です。スキルとは何か、いつ使用するか、どのように実行するかをエージェントに伝えます。

次の 2 つの部分で構成されます。

- YAML フロントマター
- マークダウンの本文。

**YAML フロントマター**

これがメタデータ レイヤです。エージェントのハイレベル ルーターによってインデックス登録されるのは、スキルの一部のみです。ユーザーがプロンプトを送信すると、エージェントは利用可能なすべてのスキルの説明フィールドに対してプロンプトのセマンティック マッチングを行います。

```
---
name: database-inspector
description: Use this skill when the user asks to query the database, check table schemas, or inspect user data in the local PostgreSQL instance.
---
```

主なフィールド:

- **name**: 必須ではありません。スコープ内で一意である必要があります。小文字、ハイフン可（例: `postgres-query` 、 `pr-reviewer` ）。指定しない場合は、デフォルトでディレクトリ名になります。
- **description**: 必須の最も重要なフィールドです。これは「トリガー フレーズ」として機能します。LLM がセマンティックな関連性を認識できる程度に説明的である必要があります。「データベース ツール」のような曖昧な説明では不十分です。「ローカル PostgreSQL データベースに対して読み取り専用の SQL クエリを実行して、ユーザーまたはトランザクション データを取得します。Use this for debugging data states" を使用すると、スキルが正しく取得されます。

**マークダウン本文**

本文には手順が記載されています。これは、ファイルに保存された「プロンプト エンジニアリング」です。スキルが有効になると、このコンテンツがエージェントのコンテキスト ウィンドウに挿入されます。

本文には次の内容を含める必要があります。

1. 目標: スキルで達成できる内容を明確に記述します。
2. 手順: ステップごとのロジック。
3. 例: モデルのパフォーマンスをガイドする入出力の少数ショットの例。
4. 制約: 「しない」ルール（「DELETE クエリを実行しない」など）。

**SKILL.md 本文の例:**

```
Database Inspector

Goal
To safely query the local database and provide insights on the current data state.

Instructions
- Analyze the user's natural language request to understand the data need.
- Formulate a valid SQL query.
 - CRITICAL: Only SELECT statements are allowed.
- Use the script scripts/query_runner.py to execute the SQL.
 - Command: python scripts/query_runner.py "SELECT * FROM..."
- Present the results in a Markdown table.

Constraints
- Never output raw user passwords or API keys.
- If the query returns > 50 rows, summarize the data instead of listing it all.
```

## スクリプトの統合

スキルの最も強力な機能の一つは、スクリプトへの実行の委任です。これにより、エージェントは LLM が直接行うことが難しい、または不可能なアクション（バイナリ実行、複雑な数学的計算、レガシー システムとのやり取りなど）を実行できます。

スクリプトは `scripts/` サブディレクトリに配置されます。 `SKILL.md` は相対パスでそれらを参照します。

## 5\. 作成スキル

このセクションの目標は、Antigravity に統合されるスキルを構築し、リソースやスクリプトなどのさまざまな機能を段階的に示すことです。

スキルは、こちらの Github リポジトリ（ [https://github.com/rominirani/antigravity-skills](https://github.com/rominirani/antigravity-skills) ）からダウンロードできます。

これらのスキルを `~/.gemini/antigravity/skills` フォルダまたは `/.agent/skills` フォルダに配置する方法について説明します。

## レベル 1: 基本ルーター（ git-commit-formatter ）

これをスキルの「Hello World」としましょう。

デベロッパーは、「wip」、「fix bug」、「updates」などの怠惰なコミット メッセージを記述することがよくあります。「Conventional Commits」を手動で適用するのは面倒で、忘れられることがよくあります。Conventional Commits 仕様を適用する Skill を実装してみましょう。エージェントにルールを指示するだけで、エージェントが実施者として機能できるようになります。

```
git-commit-formatter/
└── SKILL.md  (Instructions only)
```

`SKILL.md` ファイルは次のとおりです。

```
---
name: git-commit-formatter
description: Formats git commit messages according to Conventional Commits specification. Use this when the user asks to commit changes or write a commit message.
---

Git Commit Formatter Skill

When writing a git commit message, you MUST follow the Conventional Commits specification.

Format
\`<type>[optional scope]: <description>\`

Allowed Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

Instructions
1. Analyze the changes to determine the primary \`type\`.
2. Identify the \`scope\` if applicable (e.g., specific component or file).
3. Write a concise \`description\` in an imperative mood (e.g., "add feature" not "added feature").
4. If there are breaking changes, add a footer starting with \`BREAKING CHANGE:\`.

Example
\`feat(auth): implement login with google\`
```

**この例を実行する方法:**

1. ワークスペース内の任意のファイルに小さな変更を加えます。
2. チャットを開き、「Commit these changes」と入力します。
3. エージェントは git commit を実行するだけではありません。まず、git-commit-formatter スキルを有効にします。
4. 結果: 従来型の Git commit メッセージが提案されます。

たとえば、Antigravity にサンプル Python ファイルにコメントを追加するように指示したところ、 `docs: add detailed comments to demo_primes.py.` のような Git commit メッセージが生成されました。

これは「参照」パターンです。

企業プロジェクトのすべてのソースファイルに、特定の 20 行の Apache 2.0 ライセンス ヘッダーが必要になる場合があります。この静的テキストをプロンプト（または `SKILL.md` ）に直接入れるのは無駄です。スキルがインデックスに登録されるたびにトークンが消費され、モデルが法的テキストの誤字脱字を「ハルシネーション」する可能性があります。

静的テキストを `resources/` フォルダ内のプレーン テキスト ファイルにオフロードします。スキルは、必要な場合にのみこのファイルを読み取るようエージェントに指示します。

```
license-header-adder/
├── SKILL.md
└── resources/
   └── HEADER_TEMPLATE.txt  (The heavy text)
```

`SKILL.md` ファイルは次のとおりです。

```
---
name: license-header-adder
description: Adds the standard open-source license header to new source files. Use involves creating new code files that require copyright attribution.
---

# License Header Adder Skill

This skill ensures that all new source files have the correct copyright header.

## Instructions

1. **Read the Template**:
  First, read the content of the header template file located at \`resources/HEADER_TEMPLATE.txt\`.

2. **Prepend to File**:
  When creating a new file (e.g., \`.py\`, \`.java\`, \`.js\`, \`.ts\`, \`.go\`), prepend the \`target_file\` content with the template content.

3. **Modify Comment Syntax**:
  - For C-style languages (Java, JS, TS, C++), keep the \`/* ... */\` block as is.
  - For Python, Shell, or YAML, convert the block to use \`#\` comments.
  - For HTML/XML, use \`<!-- ... -->\`.
```

**この例を実行する方法:**

1. 新しいダミー Python ファイル `touch my_script.py` を作成します。
2. タイプ: `Add the license header to my_script.py` 。
3. エージェントは `license-header-adder/resources/HEADER_TEMPLATE.txt` を読み取ります。
4. コンテンツがファイルにそのまま貼り付けられます。

## レベル 3: 例による学習（json-to-pydantic）

「少数ショット」パターン。

緩いデータ（JSON API レスポンスなど）を厳密なコード（Pydantic モデルなど）に変換するには、数十もの決定が必要です。クラスにはどのような名前を付けるべきですか？ `Optional` を使用すべきですか？ `snake_case` または `camelCase` ？これらの 50 個のルールを英語で記述するのは、面倒でエラーが発生しやすくなります。

LLM はパターン マッチング エンジンです。

詳細な手順を示すよりも、優れた例（ `Input` -> `Output` ）を示す方が効果的な場合が多くあります。

```
json-to-pydantic/
├── SKILL.md
└── examples/
   ├── input_data.json   (The Before State)
   └── output_model.py   (The After State)
```

`SKILL.md` ファイルは次のとおりです。

```
---
name: json-to-pydantic
description: Converts JSON data snippets into Python Pydantic data models.
---

# JSON to Pydantic Skill

This skill helps convert raw JSON data or API responses into structured, strongly-typed Python classes using Pydantic.

Instructions

1. **Analyze the Input**: Look at the JSON object provided by the user.
2. **Infer Types**:
  - \`string\` -> \`str\`
  - \`number\` -> \`int\` or \`float\`
  - \`boolean\` -> \`bool\`
  - \`array\` -> \`List[Type]\`
  - \`null\` -> \`Optional[Type]\`
  - Nested Objects -> Create a separate sub-class.
 
3. **Follow the Example**:
  Review \`examples/\` to see how to structure the output code. notice how nested dictionaries like \`preferences\` are extracted into their own class.
 
  - Input: \`examples/input_data.json\`
  - Output: \`examples/output_model.py\`

Style Guidelines
- Use \`PascalCase\` for class names.
- Use type hints (\`List\`, \`Optional\`) from \`typing\` module.
- If a field can be missing or null, default it to \`None\`.
```

`/examples` フォルダには、JSON ファイルと出力ファイル（Python ファイル）があります。両方を以下に示します。

**input\_data.json**

```
{
   "user_id": 12345,
   "username": "jdoe_88",
   "is_active": true,
   "preferences": {
       "theme": "dark",
       "notifications": [
           "email",
           "push"
       ]
   },
   "last_login": "2024-03-15T10:30:00Z",
   "meta_tags": null
}
```

**output\_model.py**

```
from pydantic import BaseModel, Field
from typing import List, Optional

class Preferences(BaseModel):
   theme: str
   notifications: List[str]

class User(BaseModel):
   user_id: int
   username: str
   is_active: bool
   preferences: Preferences
   last_login: Optional[str] = None
   meta_tags: Optional[List[str]] = None
```

**この例を実行する方法:**

1. エージェントに JSON のスニペットを提供します（チャットに貼り付けるか、ファイルを指定します）。

`{ "product": "Widget", "cost": 10.99, "stock": null }`

1. タイプ: `Convert this JSON to a Pydantic model` 。
2. エージェントはスキルフォルダ内の `examples` ペアを確認します。
3. `output_model.py` のコーディング スタイル、インポート、構造を完全に模倣した Python クラスを生成します。これには、null 株を Optional として処理することも含まれます。

出力例（ `product_model.py` ）を以下に示します。

```
from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
   product: str
   cost: float
   stock: Optional[int] = None
```

## レベル 4: 手続き型ロジック（database-schema-validator）

これは「ツール使用」パターンです。

LLM に「このスキーマは安全ですか？」と尋ねると、SQL が正しく見えるという理由だけで、重要な主キーが欠落していても問題ないと回答する可能性があります。

このチェックを決定論的なスクリプトに委任しましょう。スキルを使用して、エージェントが作成した Python スクリプトを実行するようにルーティングします。スクリプトはバイナリ（True/False）の真理値を提供します。

```
database-schema-validator/
├── SKILL.md
└── scripts/
   └── validate_schema.py  (The Validator)
```

`SKILL.md` ファイルは次のとおりです。

```
---
name: database-schema-validator
description: Validates SQL schema files for compliance with internal safety and naming policies.
---

# Database Schema Validator Skill

This skill ensures that all SQL files provided by the user comply with our strict database standards.

Policies Enforced
1. **Safety**: No \`DROP TABLE\` statements.
2. **Naming**: All tables must use \`snake_case\`.
3. **Structure**: Every table must have an \`id\` column as PRIMARY KEY.

Instructions

1. **Do not read the file manually** to check for errors. The rules are complex and easily missed by eye.
2. **Run the Validation Script**:
  Use the \`run_command\` tool to execute the python script provided in the \`scripts/\` folder against the user's file.
 
  \`python scripts/validate_schema.py <path_to_user_file>\`

3. **Interpret Output**:
  - If the script returns **exit code 0**: Tell the user the schema looks good.
  - If the script returns **exit code 1**: Report the specific error messages printed by the script to the user and suggest fixes.
```

`validate_schema.py` ファイルは次のとおりです。

```
import sys
import re

def validate_schema(filename):
   """
   Validates a SQL schema file against internal policy:
   1. Table names must be snake_case.
   2. Every table must have a primary key named 'id'.
   3. No 'DROP TABLE' statements allowed (safety).
   """
   try:
       with open(filename, 'r') as f:
           content = f.read()
          
       lines = content.split('\n')
       errors = []
      
       # Check 1: No DROP TABLE
       if re.search(r'DROP TABLE', content, re.IGNORECASE):
           errors.append("ERROR: 'DROP TABLE' statements are forbidden.")
          
       # Check 2 & 3: CREATE TABLE checks
       table_defs = re.finditer(r'CREATE TABLE\s+(?P<name>\w+)\s*\((?P<body>.*?)\);', content, re.DOTALL | re.IGNORECASE)
      
       for match in table_defs:
           table_name = match.group('name')
           body = match.group('body')
          
           # Snake case check
           if not re.match(r'^[a-z][a-z0-9_]*$', table_name):
               errors.append(f"ERROR: Table '{table_name}' must be snake_case.")
              
           # Primary key check
           if not re.search(r'\bid\b.*PRIMARY KEY', body, re.IGNORECASE):
               errors.append(f"ERROR: Table '{table_name}' is missing a primary key named 'id'.")

       if errors:
           for err in errors:
               print(err)
           sys.exit(1)
       else:
           print("Schema validation passed.")
           sys.exit(0)
          
   except FileNotFoundError:
       print(f"Error: File '{filename}' not found.")
       sys.exit(1)

if __name__ == "__main__":
   if len(sys.argv) != 2:
       print("Usage: python validate_schema.py <schema_file>")
       sys.exit(1)
      
   validate_schema(sys.argv[1])
```

**この例を実行する方法:**

1. 不正な SQL ファイル `bad_schema.sql` を作成します。 `CREATE TABLE users (name TEXT);`
2. タイプ: `Validate bad_schema.sql` 。
3. エージェントは推測しません。スクリプトが呼び出され、失敗（終了コード 1）します。そして、「テーブル ‘users’ に主キーがないため、検証に失敗しました」というメッセージが返されます。

## レベル 5: アーキテクト（adk-tool-scaffold）

このパターンは、スキルで利用できるほとんどの機能を網羅しています。

複雑なタスクでは、ファイルの作成、テンプレートの適用、ロジックの記述など、これまで見てきたすべての操作を組み合わせた一連の操作が必要になることがよくあります。ADK（Agent Development Kit）用の新しいツールを作成するには、これらすべてが必要です。

以下の情報を組み合わせます。

- スクリプト（ファイルの作成/スキャフォールディングを処理するため）
- テンプレート（リソースのボイラープレートを処理するため）
- 例（ロジック生成をガイドするため）。
```
adk-tool-scaffold/
├── SKILL.md
├── resources/
│   └── ToolTemplate.py.hbs (Jinja2 Template)
├── scripts/
│   └── scaffold_tool.py    (Generator Script)
└── examples/
    └── WeatherTool.py      (Reference Implementation)
```

`SKILL.md` ファイルを以下に示します。 [スキル リポジトリ](https://github.com/rominirani/antigravity-skills/tree/main) を参照して、スクリプト、リソース、例のフォルダにあるファイルを確認できます。この特定のスキルについては、 `adk-tool-scaffold` スキルをご覧ください。

```
---
name: adk-tool-scaffold
description: Scaffolds a new custom Tool class for the Agent Development Kit (ADK).
---

# ADK Tool Scaffold Skill

This skill automates the creation of standard \`BaseTool\` implementations for the Agent Development Kit.

Instructions

1. **Identify the Tool Name**:
  Extract the name of the tool the user wants to build (e.g., "StockPrice", "EmailSender").
 
2. **Review the Example**:
  Check \`examples/WeatherTool.py\` to understand the expected structure of an ADK tool (imports, inheritance, schema).

3. **Run the Scaffolder**:
  Execute the python script to generate the initial file.
 
  \`python scripts/scaffold_tool.py <ToolName>\`

4. **Refine**:
  After generation, you must edit the file to:
  - Update the \`execute\` method with real logic.
  - Define the JSON schema in \`get_schema\`.
 
Example Usage
User: "Create a tool to search Wikipedia."
Agent:
1. Runs \`python scripts/scaffold_tool.py WikipediaSearch\`
2. Editing \`WikipediaSearchTool.py\` to add the \`requests\` logic and \`query\` argument schema.
```

**この例の実行方法:**

1. タイプ: `Create a new ADK tool called StockPrice to fetch data from an API` 。
2. ステップ 1（スキャフォールディング）: エージェントが Python スクリプトを実行します。これにより、正しいクラス構造、インポート、クラス名 `StockPriceTool` を持つ `StockPriceTool.py` が即座に作成されます。
3. ステップ 2（実装）: エージェントが作成したファイルを「読み取り」ます。 `# TODO: Implement logic.` を確認できます
4. ステップ 3（ガイダンス）: ツール引数の JSON スキーマを定義する方法がわからない。 `examples/WeatherTool.py` を確認します。
5. 完了: ファイルを編集して `requests.get(...)` を追加し、ADK スタイルと完全に一致するようにスキーマでティッカー引数を定義します。

## 6\. 完了

これで、反重力スキルに関するラボが完了し、次のスキルが作成されました。

- Git commit フォーマッタ。
- ライセンス ヘッダーの追加ツール。
- JSON から Pydantic。
- データベース スキーマ バリデータ。
- ADK ツールのスキャフォールディング。

エージェント スキルは、Antigravity がユーザーのやり方でコードを記述し、ルールに従い、ツールを使用するのに最適な方法です。

## リファレンス ドキュメント

- [Codelab: Google Antigravity を使ってみる](https://codelabs.developers.google.com/getting-started-google-antigravity?hl=ja)
- 公式サイト: [https://antigravity.google/](https://antigravity.google/?hl=ja)
- ドキュメント: [https://antigravity.google/docs](https://antigravity.google/docs?hl=ja)
- ダウンロード: [https://antigravity.google/download](https://antigravity.google/download?hl=ja)
- Antigravity Skills のドキュメント: [https://antigravity.google/docs/skills](https://antigravity.google/docs/skills?hl=ja)

[戻る](https://codelabs.developers.google.com/getting-started-with-antigravity-skills?hl=ja#)