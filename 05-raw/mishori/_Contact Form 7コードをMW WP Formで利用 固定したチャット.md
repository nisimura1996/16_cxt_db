> From: https://gemini.google.com/app/f21e3d62309f9eea

# you asked

｛#コード｝はコンタクトフォーム７用ですがMW WP Formでも使用したい

#コード
<?php
if ( ! defined( 'ABSPATH' ) ) exit;

function handler_tag_privacy_policy( $tag ) {
	ob_start();

	// 「プライバシー ポリシー」ページのコンテンツを取得する
	$privacy_page = get_page_by_path( 'privacy-policy' );
	if ( $privacy_page ) {
		echo apply_filters( 'the_content', $privacy_page->post_content );
	}

	$output = ob_get_clean();
	return $output;
}

function add_tag_privacy_policy() {
	wpcf7_add_form_tag( 'privacy_policy', 'handler_tag_privacy_policy' );
}
add_action( 'wpcf7_init', 'add_tag_privacy_policy' );
?>

---

# gemini response

MW WP FormはContact Form 7と異なり、独自のフォームタグエンジンではなく、**通常のWordPressショートコード**をフォーム作成画面でそのまま展開できる仕様になっています。

そのため、CF7専用のフック（`wpcf7_init`や`wpcf7_add_form_tag`）を取り除き、WordPress標準のショートコードAPI（`add_shortcode`）を使った形に書き換えるのが最もシンプルで確実です。

### MW WP Form用のコード

以下のコードをテーマの `functions.php` に追加してください。

```php
<?php
if ( ! defined( 'ABSPATH' ) ) exit;

function shortcode_privacy_policy() {
	ob_start();

	// 「プライバシー ポリシー」ページのコンテンツを取得する
	$privacy_page = get_page_by_path( 'privacy-policy' );
	if ( $privacy_page ) {
		echo apply_filters( 'the_content', $privacy_page->post_content );
	}

	$output = ob_get_clean();
	return $output;
}

// 標準のショートコードとして登録
add_shortcode( 'privacy_policy', 'shortcode_privacy_policy' );
?>
```

### 使い方

MW WP Formのフォーム編集画面（テキストエリア内）の、プライバシーポリシーを表示したい場所に以下のショートコードを記述します。

```text
[privacy_policy]
```

### 実装時のポイント

  * **HTMLの出力:** 取得したコンテンツには `apply_filters( 'the_content', ... )` がかかっているため、固定ページで作成したHTMLタグ（`p`タグなど）がそのまま出力されます。
  * **レイアウト調整:** 利用規約のようによくある「スクロール枠」の中に表示させたい場合は、フォーム編集画面側で以下のようにHTMLで囲み、CSSで高さを制限すると綺麗にまとまります。

<!-- end list -->

```html
<div class="privacy-scroll-box" style="height: 200px; overflow-y: scroll; border: 1px solid #ccc; padding: 15px;">
    [privacy_policy]
</div>
```

合わせて、このプライバシーポリシーに対する「同意する」チェックボックスの設置や、MW WP Formでの必須バリデーション設定についてサポートは必要でしょうか？

---

# you asked

<div class="privacy-scroll-box" style="height: 200px; overflow-y: scroll; border: 1px solid #ccc; padding: 15px;">
    [privacy_policy]
</div>を追記しましたがボーダーなどを反映されていますが、コンテンツは表示されません

---

# gemini response

枠（ボーダー）だけが表示されて中身が空欄になる場合、ショートコード自体は動作しているものの、\*\*「WordPressが指定されたページ（コンテンツ）を見つけられていない」\*\*可能性が最も高いです。

原因を特定し確実に表示させるため、以下の2点をご確認ください。

### 1\. ページのスラッグ（URL）と公開状態の確認

前回のコードは、URLの一部（スラッグ）が `privacy-policy` となっている固定ページを探しにいく仕様でした。

  * **スラッグは正しいか？**：固定ページ一覧から該当のページを開き、URL（パーマリンク）が `privacy` や `policy` など、別のものになっていないか確認してください。
  * **公開されているか？**：ページが「下書き」や「非公開」になっていると取得できません。「公開済」になっているか確認してください。

-----

### 2\. より確実な「ページID」を使ったコードへの変更

スラッグ（URL）は変更される可能性があるため、**「ページID（数字）」で取得する形**に変更すると確実です。また、原因がすぐ分かるように、取得できなかった場合のエラーメッセージが出るようにコードを改良しました。

以下の手順でお試しください。

#### 手順①：ページIDを調べる

WordPressの管理画面「固定ページ一覧」から、プライバシーポリシーの編集画面を開きます。
その時のブラウザのURLバーを見て、`post=〇〇` の **〇〇の数字** をメモします。
（例：`post=15&action=edit` なら IDは `15` です）

#### 手順②：functions.php のコードを書き換える

前回のコードを以下に丸ごと差し替えてください。

```php
<?php
if ( ! defined( 'ABSPATH' ) ) exit;

function shortcode_privacy_policy() {
	ob_start();

	// ▼ ここに先ほど調べたプライバシーポリシーページの「ID（半角数字）」を入力してください
	$page_id = 15; 
	
	$privacy_page = get_post( $page_id );

	// ページが存在し、かつ「公開」状態の場合のみ出力
	if ( $privacy_page && $privacy_page->post_status === 'publish' ) {
		echo apply_filters( 'the_content', $privacy_page->post_content );
	} else {
		// 取得失敗時のデバッグ用メッセージ（確認後に消してもOKです）
		echo '<p style="color:red;">※プライバシーポリシーのページを取得できません。functions.phpのページID（' . $page_id . '）が正しいか確認してください。</p>';
	}

	$output = ob_get_clean();
	return $output;
}

// 標準のショートコードとして登録
add_shortcode( 'privacy_policy', 'shortcode_privacy_policy' );
?>
```

### ※もし画面に `[privacy_policy]` という文字がそのまま出ている場合

中身が真っ白ではなく、`[privacy_policy]` というショートコードの文字列がそのままブラウザ上に表示されてしまっている場合は、MW WP Form側でショートコードが展開されていない状態です。
その場合は状況が変わってきますので、「真っ白（枠だけ）」か「文字がそのまま出ているか」を教えていただけますでしょうか？

---

# you asked

真っ白（枠だけ）

---

# gemini response

`[privacy_policy]`という文字がそのまま出ているわけではなく「真っ白（枠だけ）」になっているということは、**ショートコード自体は正常に動作（実行）しています。**

MW WP Form側はショートコードを認識して処理しましたが、「肝心の文章データを引っ張ってこれなかった」または「出力する直前で文章が消えてしまった」状態です。

原因として、WordPressのフィルターフック（`the_content`）が他のプラグインやテーマの機能と衝突して、中身を空っぽにしてしまっている可能性が非常に高いです。

### 解決策：フィルターを回避するコードに変更する

`apply_filters( 'the_content', ... )` の使用をやめ、シンプルに改行だけを反映させる `wpautop()` に変更することで、衝突を回避できます。

以下のコードを `functions.php` に上書きしてください。
※ `$page_id = 15;` の数字の部分は、実際のプライバシーポリシーの固定ページID（URLの post=〇〇 の数字）に書き換えてください。

```php
<?php
if ( ! defined( 'ABSPATH' ) ) exit;

function shortcode_privacy_policy() {
	// ▼ 実際のプライバシーポリシーページのID（半角数字）に変更してください
	$page_id = 15; 
	
	$privacy_page = get_post( $page_id );

	if ( $privacy_page && $privacy_page->post_status === 'publish' ) {
		// the_contentフィルターを避け、wpautopでPタグ（改行）のみ自動付与する
		return wpautop( $privacy_page->post_content );
	}

	// IDが間違っている等の場合はこのテキストが出力されます
	return '<p style="color:red;">ページデータを取得できませんでした。ID（' . $page_id . '）を確認してください。</p>';
}

add_shortcode( 'privacy_policy', 'shortcode_privacy_policy' );
?>
```

### 上記のコードでもまだ「真っ白」になる場合

Elementorなどの「ページビルダープラグイン」を使ってプライバシーポリシーを作成している場合、通常の `post_content` に文章データが保存されないため、真っ白になることがあります。

ページビルダープラグインは何か使用されていますか？

---

# you asked

すべて選択
プラグイン説明自動更新Advanced Custom Fields を選択
Advanced Custom Fields
無効化
パワフル、プロフェッショナル、直感的なフィールドで WordPress をカスタマイズ。
バージョン 6.7.0 | 作者: WP Engine | 詳細を表示
自動更新を有効化する
自動更新は停止中です
Advanced Editor Tools を選択
Advanced Editor Tools
無効化 | 設定
ブロックエディター (Gutenberg) とクラシックエディター (TinyMCE) を拡張、強化します。
バージョン 5.9.2 | 作者: Automattic | 詳細を表示
自動更新を有効化する
自動更新は停止中です
Akismet Anti-spam: Spam Protection を選択
Akismet Anti-spam: Spam Protection
設定 | 無効化
何百万もの利用実績がある Akismet はあなたのブログをスパムから保護する最良の方法といえるでしょう。このサイトでの設定は完了しており Akismet が常時保護しています。
バージョン 5.6 | 作者: Automattic - Anti-spam Team | 詳細を表示
自動更新を有効化する
自動更新は停止中です
Aurora Heatmap を選択
Aurora Heatmap
無効化
オーロラのように美しい、プラグインだけで完結するシンプルな WordPress 用ヒートマップです。
バージョン 1.7.1 | 作者: R3098 | 詳細を表示
自動更新を有効化する
自動更新は停止中です
BBQ Firewall を選択
BBQ Firewall
Go Pro | Settings | 無効化
BBQ is a blazing fast firewall that protects WordPress against a wide range of threats.
バージョン 20251120 | 作者: Jeff Starr | 詳細を表示 | Homepage | Rate this plugin »
自動更新を有効化する
自動更新は停止中です
新バージョンの BBQ Firewall が利用できます。バージョン 20260205 の詳細を表示するか、更新してください。
Converter for Media を選択
Converter for Media
設定 | 無効化 | PRO にアップグレード
Speed up your website by using our WebP & AVIF Converter. Optimize images and serve WebP and AVIF images instead of standard formats!
バージョン 6.5.3 | 作者: matt plugins | 詳細を表示
自動更新を有効化する
自動更新は停止中です
Custom Post Type UI を選択
Custom Post Type UI
このサイトについて | ヘルプ | 無効化
カスタム投稿タイプやカスタムタクソノミを登録する管理 UI パネル
バージョン 1.18.3 | 作者: WebDevStudios | 詳細を表示
自動更新を有効化する
自動更新は停止中です
LIQUID SPEECH BALLOON を選択
LIQUID SPEECH BALLOON
設定 | 無効化
会話形式の吹き出しデザインを Gutenberg ビジュアルエディターで作成できます。
バージョン 1.2.5 | 作者: LIQUID DESIGN Ltd. | 詳細を表示
自動更新を有効化する
自動更新は停止中です
MW WP Form を選択
MW WP Form
無効化
MW WP Form はショートコードベースのフォームプラグインです。多くの機能を持っており、例えば、多くのバリデーションルール、問い合わせデータの保存、そしてグラフ機能集計などを使用することができます。
バージョン 5.1.0 | 作者: websoudan | 詳細を表示
自動更新を有効化する
自動更新は停止中です
Post Type Switcher を選択
Post Type Switcher
無効化
WordPress で投稿タイプを変更する簡単な方法
バージョン 4.0.1 | 作者: Triple J Software, Inc. | 詳細を表示
自動更新を有効化する
自動更新は停止中です
reCAPTCHA for MW WP Form を選択
reCAPTCHA for MW WP Form
無効化
You can use reCAPTCHA v3 on the MW WP Form.
バージョン 1.1.7 | 作者: Nakashima Masahiro | 詳細を表示
自動更新を有効化する
自動更新は停止中です
SEO SIMPLE PACK を選択
SEO SIMPLE PACK
無効化
とてもシンプルなSEOプラグインです。ページごとのmetaタグやOGPタグを簡単に設定・カスタマイズできます。
バージョン 3.6.2 | 作者: LOOS,Inc. | 詳細を表示
自動更新を有効化する
自動更新は停止中です
VK Blocks を選択
VK Blocks
設定 | 無効化
ブロックエディタを拡張するプラグインです。
バージョン 1.115.2.1 | 作者: Vektor,Inc. | 詳細を表示
自動更新を有効化する
自動更新は停止中です
新バージョンの VK Blocks が利用できます。バージョン 1.116.2.0 の詳細を表示するか、更新してください。
WP File Manager を選択
WP File Manager
Buy Pro | Donate | 無効化
Manage your WP files.
バージョン 8.0.2 | 作者: mndpsingh287 | 詳細を表示
自動更新を有効化する
自動更新は停止中です
WP Multibyte Patch を選択
WP Multibyte Patch
無効化
WP Multibyte Patch は、本家版、日本語版 WordPress のマルチバイト文字の取り扱いに関する不具合の累積的修正と強化を行うプラグインです。 » 詳しい説明を読む
バージョン 2.9.3 | 作者: 倉石 政典 | 詳細を表示
自動更新を有効化する
自動更新は停止中です
WPvivid Backup Plugin を選択
WPvivid Backup Plugin
設定 | 無効化
WordPress サイトのクローンやコピー、新しいホスト (新しいドメイン) への移動や移行、バックアップのスケジュール設定、主要なリモートストレージへのバックアップの転送を、すべて1つで行います。
バージョン 0.9.124 | 作者: WPvivid Backup & Migration | 詳細を表示
自動更新を有効化する
自動更新は停止中です
XML Sitemap & Google News を選択
XML Sitemap & Google News
設定 | 無効化
Feed the hungry spiders in compliance with the XML Sitemap and Google News protocols.
バージョン 5.7.2 | 作者: RavanH | 詳細を表示 | ヘルプ | Rate ★★★★★
自動更新を有効化する
自動更新は停止中です
XO Security を選択
XO Security
設定 | 無効化
XO Security は、ログイン関連のセキュリティを強化するプラグインです。
バージョン 3.10.8 | 作者: Xakuro | 詳細を表示
自動更新を有効化する
自動更新は停止中です
Yoast Duplicate Post を選択
Yoast Duplicate Post
設定 | 無効化
強力な書き換えと再公開機能を含む、投稿と固定ページ複製用の頼りになるツール。
バージョン 4.5 | 作者: Enrico Battocchi & Team Yoast | 詳細を表示 | ドキュメント
自動更新を有効化する
自動更新は停止中です

---

# gemini response

プラグイン一覧を教えていただき、ありがとうございます！

Elementorのような特殊なページビルダープラグインは使用されておらず、**「VK Blocks」** をお使いとのことですので、プライバシーポリシーはWordPress標準のブロックエディタで作られている状態ですね。

この環境で「枠だけ表示されて中身が真っ白になる」場合、原因はほぼ確実に **「プログラムが指定したページを見つけられていない（スラッグやIDが間違っている）」** ことです。

`functions.php` のコードを何度も書き換えるのは大変だと思いますので、**フォーム側のショートコードで「ページID」を直接指定できる**、より便利で確実なコードに作り直しました。

以下の手順で進めてみてください。

### 手順1：functions.php のコードを差し替える

現在追記していただいたコードを消去し、以下のコードに丸ごと差し替えてください。

```php
<?php
if ( ! defined( 'ABSPATH' ) ) exit;

function mw_shortcode_privacy_policy( $atts ) {
	// ショートコードの属性（ID）を取得
	$atts = shortcode_atts( array(
		'id' => '',
	), $atts, 'privacy_policy' );

	$page_id = intval( $atts['id'] );

	// IDが入力されていない場合のエラー
	if ( ! $page_id ) {
		return '<p style="color:red; font-weight:bold;">※エラー: ショートコードに固定ページのIDを指定してください。例: [privacy_policy id="15"]</p>';
	}

	$privacy_page = get_post( $page_id );

	// ページが見つからない、または公開されていない場合のエラー
	if ( ! $privacy_page || $privacy_page->post_status !== 'publish' ) {
		return '<p style="color:red; font-weight:bold;">※エラー: 指定されたID（' . $page_id . '）のページが見つからないか、非公開状態です。</p>';
	}

	// VK Blocksなどのブロックエディタの装飾を正常に出力するための処理
	$content = apply_filters( 'the_content', $privacy_page->post_content );
	$content = str_replace( ']]>', ']]&gt;', $content );

	return $content;
}

// ショートコードを登録
add_shortcode( 'privacy_policy', 'mw_shortcode_privacy_policy' );
?>
```

-----

### 手順2：プライバシーポリシーの「ページID」を調べる

1.  WordPressの管理画面から「固定ページ」\>「一覧」を開きます。
2.  プライバシーポリシーのページタイトルにマウスを合わせ、**「編集」** をクリックします。
3.  その時のブラウザ上部のURL（アドレスバー）を見てください。
    `post=〇〇` という部分の **〇〇の数字** がページIDです。（例：`post=32` なら IDは `32`）

-----

### 手順3：MW WP Formにショートコードを設置する

MW WP Formの編集画面（スクロール枠のHTML）を以下のように書き換えます。
**※ `id="〇〇"` の部分に、手順2で調べた数字を入れてください。**

```html
<div class="privacy-scroll-box" style="height: 200px; overflow-y: scroll; border: 1px solid #ccc; padding: 15px; margin-bottom: 20px;">
    [privacy_policy id="〇〇"]
</div>
```

*(例: IDが 32 だった場合は `[privacy_policy id="32"]` となります)*

これで、IDさえ合っていれば必ず文章（VK Blocksの装飾も含む）が表示されるか、万が一間違っていても赤文字でエラー理由が画面に出力されるようになります。

こちらの設定で無事に文章は表示されましたでしょうか？確認できましたら、次は「同意する」チェックボックスの設置に進みましょうか？

---

# you asked

26、privacy、テンプレートはmyTemplateで
myTemplateからpage/privacy.phpを読み込んでいます。

---

# gemini response

なるほど、原因がはっきりと分かりました！

WordPressの管理画面（エディタ）に直接文章を打ち込んでいるのではなく、**テーマファイル内の `page/privacy.php` を読み込んでいる**状態ですね。

これまでのコードは「データベース上（管理画面のエディタ内）の文章」を取得する処理だったため、エディタが空欄（または空に近い状態）であるこの構成では、枠だけが表示されて中身が真っ白になってしまっていました。

### 解決策：テンプレートファイルを直接読み込むショートコード

管理画面のデータではなく、直接 `page/privacy.php` の中身を出力するように `functions.php` のコードを書き換えます。これで確実に表示されるはずです。

現在 `functions.php` に追記してあるコードを削除し、以下のコードに差し替えてください。

```php
<?php
if ( ! defined( 'ABSPATH' ) ) exit;

function shortcode_privacy_policy_from_file() {
	// 出力のバッファリングを開始
	ob_start();

	// テーマ内の 'page/privacy.php' を読み込む
	get_template_part( 'page', 'privacy' ); 
	// ※ 'page/privacy.php' というファイル名であれば get_template_part( 'page/privacy' ) でも可

	// 読み込んだ内容を変数に格納
	$output = ob_get_clean();

	// 万が一ファイルが見つからない、または空の場合のエラーメッセージ
	if ( empty( trim( $output ) ) ) {
		return '<p style="color:red; font-weight:bold;">※エラー: テンプレートファイル page/privacy.php の内容を取得できませんでした。</p>';
	}

	return $output;
}

// ショートコードを登録
add_shortcode( 'privacy_policy', 'shortcode_privacy_policy_from_file' );
?>
```

### MW WP Form側の設定

MW WP Formの編集画面には、ID等の指定は不要になりますので、シンプルに以下のように記述してください。

```html
<div class="privacy-scroll-box" style="height: 200px; overflow-y: scroll; border: 1px solid #ccc; padding: 15px;">
    [privacy_policy]
</div>
```

-----

これで `page/privacy.php` に記述されているHTMLタグごと、スクロール枠の中に展開されるようになります。

無事にプライバシーポリシーの内容が表示されましたでしょうか？ 確認できましたら、次のステップとしてMW WP Formでの「同意する」チェックボックスの設置方法へ進みましょうか？

---

# you asked

読み込みが終わらなくなりました

---

# gemini response

読み込みが終わらなくなってしまったとのこと、大変申し訳ありません！
それは\*\*「無限ループ」**または**「ページ全体の二重読み込み」\*\*が発生して処理がパンクしている状態です。

### 🚨 【至急】まずはサイトを復旧させてください

`functions.php` に先ほど追記したコード（`shortcode_privacy_policy_from_file` の部分）を**すべて削除**して保存してください。これでサイトの読み込みは元に戻ります。

-----

### 原因について

`page/privacy.php` の中には、プライバシーポリシーの文章だけでなく、**ヘッダー（`get_header()`）やフッター、その他のレイアウト用のコード**が含まれていませんか？

先ほどのコードは「そのファイルを丸ごとフォームの中に読み込む」という処理だったため、フォームの中にサイト全体（ヘッダーからフッターまで）が読み込まれてしまい、HTML構造が完全に崩壊して無限ループを引き起こしてしまいました。

### 正しい解決策：文章だけの「専用ファイル」を作る

この構成（テキストがエディタではなくPHPファイルに直書きされている状態）でフォーム内に表示させるには、\*\*「文章のHTMLだけが書かれた部品ファイル」\*\*を作るのが一番スマートで確実な方法です。

以下の3ステップで実装してみてください。

#### ステップ1：テーマ内に新しい部品ファイルを作る

ご利用のテーマフォルダ（`page/privacy.php`があるのと同じ階層など）に、新しく **`privacy-text.php`** という空のファイルを作成してください。

そして、`page/privacy.php` の中に書かれている\*\*「プライバシーポリシーの文章部分（HTML）だけ」\*\*を切り取って、この `privacy-text.php` に貼り付けて保存します。（※`get_header()`などは絶対に入れないでください）

#### ステップ2：元のページで部品を読み込む

元の `page/privacy.php` の、文章を切り取って空いたスペースに以下の1行を記述します。

```php
<?php get_template_part( 'privacy-text' ); ?>
```

これで、実際のプライバシーポリシーのページは今まで通りに表示されます。

#### ステップ3：functions.php を修正する

`functions.php` に、以下の**安全なコード**を追記してください。今回はヘッダー等が含まれない純粋なテキストファイルだけを読み込むので、フリーズしません。

```php
<?php
if ( ! defined( 'ABSPATH' ) ) exit;

function shortcode_privacy_policy_safe() {
	ob_start();

	// 先ほど作成した「文章だけのファイル」を読み込む
	get_template_part( 'privacy-text' ); 

	$output = ob_get_clean();
	return $output;
}
add_shortcode( 'privacy_policy', 'shortcode_privacy_policy_safe' );
?>
```

-----

MW WP Form側の設定は、先ほどと同じ `[privacy_policy]` のままで大丈夫です。

お手数をおかけして申し訳ありません。この「テンプレートパーツ化」の手法であれば確実に解決できますので、サイトが復旧できたらぜひお試しください。無事に表示されるかお待ちしております！

---

# you asked

下記を使用するとCSSが反映されているので、テキストのみを生成する事は可能？
function shortcode_privacy_policy_safe() {
	ob_start();

	// 先ほど作成した「文章だけのファイル」を読み込む
	get_template_part( 'page/privacy-text' ); 

	$output = ob_get_clean();
	return $output;
}
add_shortcode( 'privacy_policy', 'shortcode_privacy_policy_safe' );

---

# gemini response

無事にファイルの読み込みができたようで安心しました！無限ループも解消されて良かったです。

HTMLのタグ（`<div>` や `<p>`、見出しタグなど）やそこに付与されているクラス名ごと読み込まれているため、テーマのCSSが効いてしまっている状態ですね。

PHPの機能を使って\*\*「HTMLタグ（CSS）をすべて引っぺがし、純粋なテキストのみにする」\*\*ことは可能です！

### テキストのみを出力するコード

現在の `functions.php` のコードを、以下の内容に書き換えてください。

```php
<?php
if ( ! defined( 'ABSPATH' ) ) exit;

function shortcode_privacy_policy_safe() {
	ob_start();

	// 先ほど作成した「文章だけのファイル」を読み込む
	get_template_part( 'page/privacy-text' ); 

	$output = ob_get_clean();

	// 1. HTMLタグ（装飾やCSSクラス）をすべて除去して純粋なテキストにする
	$text_only = wp_strip_all_tags( $output );

	// 2. そのままだと文章が繋がってしまうため、テキストの改行を <br> に変換して見やすくする
	return nl2br( $text_only );
}
add_shortcode( 'privacy_policy', 'shortcode_privacy_policy_safe' );
?>
```

### 追加した処理の解説

  * **`wp_strip_all_tags()`**: WordPressに用意されている関数で、読み込んだデータからHTMLタグをすべて綺麗に削除します。これでCSSが一切当たらなくなります。
  * **`nl2br()`**: HTMLタグを消去すると、ブラウザ上では改行が無視されて文字がぎっしり詰まって見えてしまいます。これを防ぐため、元のテキストの改行部分にだけ `<br>`（改行タグ）を自動で補う処理を入れています。

-----

これで、スクロール枠の中には「テーマのCSSの影響を受けない、シンプルなテキスト」だけが表示されるはずです。

無事に綺麗なテキスト表示になりましたら、いよいよMW WP Formでの「プライバシーポリシーに同意する」チェックボックスの設置と、必須項目（バリデーション）の設定に進みましょうか？

---

# you asked

クラス名を無くしたHTMLタグのみ出力したい

---

# gemini response

なるほど！HTMLの構造（見出しの `<h2>` や、段落の `<p>`、リストの `<ul>` など）はしっかり残して読みやすくしつつ、テーマのCSSが当たってしまう原因である **`class` や `id` などの属性だけを狙って削除したい** ということですね。

それであれば、正規表現を使ってHTMLタグの中から特定の属性（クラス名など）だけを取り除く処理を加えるのがベストです。

現在の `functions.php` のコードを、以下のように書き換えてみてください。

```php
<?php
if ( ! defined( 'ABSPATH' ) ) exit;

function shortcode_privacy_policy_safe() {
	ob_start();

	// 先ほど作成した「文章だけのファイル」を読み込む
	get_template_part( 'page/privacy-text' ); 

	$output = ob_get_clean();

	// 正規表現を使って class、id、style 属性だけをすべて削除する
	// ※ href（リンク）や src（画像）などの必要な属性は残ります
	$output = preg_replace( '/\s+(class|id|style)=["\'][^"\']*["\']/i', '', $output );

	return $output;
}
add_shortcode( 'privacy_policy', 'shortcode_privacy_policy_safe' );
?>
```

### 追加した処理の解説

  * **`preg_replace()`**: 文字列の中から指定したパターンを見つけて、別の文字（今回は空文字）に置き換える関数です。
  * **`/\s+(class|id|style)=["\'][^"\']*["\']/i`**: 少し複雑に見えますが、「半角スペースの後に続く `class="..."` や `id="..."` や `style="..."` という記述を丸ごと見つけ出す」という指示です。

これで、リンク（`<a href="...">`）などの機能的に必要な部分は残しつつ、デザインに影響を与えるクラス名だけが綺麗に剥がれ落ちたHTMLが出力されます。

テーマのCSSに引っ張られず、段落や見出しの構造を保った状態で表示されるようになったか確認してみてください。問題なく表示されましたら、MW WP Formの「同意する」チェックボックスの設置と必須設定に進みましょうか？

---

# you asked

変更を保存中にエラーが発生しました。もう一度お試しください。問題が解決しない場合は、FTP 経由でファイルを手動で更新する必要がある可能性があります。

---

# gemini response

WordPressの管理画面から保存しようとした際に、そのエラーが出たのですね。驚かれたかもしれませんが、サイト自体は壊れていないので安心してください。

エラーの原因は主に以下の2つが考えられます。

1. **サーバーのセキュリティ（WAF）による誤検知:** 今回追加したコードの「正規表現（`preg_replace...`）」の記号の並びが、レンタルサーバーのセキュリティ機能に「不正な書き換え操作」と誤検知されて、保存がブロックされた可能性が非常に高いです。
2. **`<?php` の重複:** コードを貼り付けた際、すでにファイルに書かれている `<?php` の内側に、さらに `<?php` を貼り付けてしまい、構文エラーとしてWordPressが安全のために保存を止めたケースです。

エラーメッセージにある通り「FTP経由」でファイルを上書きするのが確実ですが、**WordPressの左メニューにある「WP File Manager」** を使えば、面倒なFTPソフトの設定なしで、今すぐ安全に保存を突破できます。

### WP File Managerを使った解決手順

1. 左メニューから **「WP File Manager」** をクリックして開きます。
2. フォルダが並んでいる画面が出たら、以下の順にダブルクリックして進みます。
   `wp-content` ＞ `themes` ＞ `（現在使っているテーマ名のフォルダ）`
3. その中にある **`functions.php`** を見つけて **右クリック** し、「**Code Editor**（または Edit）」を選択します。
4. エディターが開いたら、適切な場所に先ほどのコードを貼り付けます。
   ※この時、一番上の `<?php` が連続して二重にならないようにご注意ください（不要な場合はコード内の `<?php` と `?>` は削って中身だけ貼り付けます）。
5. 「Save & Close（保存して閉じる）」をクリックします。

WP File Managerからの直接保存であれば、テーマファイルエディター特有のセキュリティ制限を回避できることが多いです。

無事に保存できましたでしょうか？もし「WP File Managerでもエラーが出る」という場合は、セキュリティに引っかからない別のコードの書き方（正規表現を使わない方法）に変更してご提案しますので、お知らせください。

---

# you asked

正規表現を使わない方法

---

# gemini response

サーバーのセキュリティ（WAF）によるブロックですね。`preg_replace` のような正規表現の記号の羅列は、ハッカーの攻撃コードと似ているため、レンタルサーバー側で誤検知されて保存が弾かれることがよくあります。

正規表現を使わずに、**WordPressに標準搭載されている「安全なHTMLフィルター機能（`wp_kses`）」** を使う方法に変更しましょう。

この方法ならセキュリティの警告に引っかからず、管理画面からでも安全に保存できます。

### WordPress標準機能（wp\_kses）を使ったコード

現在 `functions.php` に追記しようとしていたコードを、以下の内容に丸ごと差し替えて保存してみてください。

```php
<?php
if ( ! defined( 'ABSPATH' ) ) exit;

function shortcode_privacy_policy_safe() {
	ob_start();

	// 先ほど作成した「文章だけのファイル」を読み込む
	get_template_part( 'page/privacy-text' ); 

	$output = ob_get_clean();

	// 許可するHTMLタグを指定します。
	// ※ここに書かれていない class、id、style などの属性は「すべて自動的に削除」されます。
	$allowed_html = array(
		'p'      => array(),
		'br'     => array(),
		'h1'     => array(),
		'h2'     => array(),
		'h3'     => array(),
		'h4'     => array(),
		'ul'     => array(),
		'ol'     => array(),
		'li'     => array(),
		'strong' => array(),
		'b'      => array(),
		'span'   => array(),
		'div'    => array(),
		'a'      => array(
			'href'   => array(), // リンクのURLだけは残す
			'target' => array(),
			'rel'    => array()
		),
		'table'  => array(),
		'tbody'  => array(),
		'tr'     => array(),
		'th'     => array(),
		'td'     => array(),
	);

	// wp_kses() で、許可したタグと属性以外を綺麗に取り除く
	$output = wp_kses( $output, $allowed_html );

	return $output;
}
add_shortcode( 'privacy_policy', 'shortcode_privacy_policy_safe' );
?>
```

### このコードの仕組み

`wp_kses()` は、指定した「許可リスト」以外のHTMLタグや属性をすべて弾き飛ばす、WordPressの強力なセキュリティ関数です。

上記のように `'p' => array()` とだけ書いておくと、「`<p>` タグ自体は許可するけれど、その中にある `class="..."` などの属性は許可していないので削除する」という動きをしてくれます（`<a>` タグの `href` など、リンクとして必要なものだけ残す設定にしています）。

正規表現の記号を使っていないため、サーバーのWAFにも弾かれず、一番WordPressらしい安全な処理方法です。

こちらで無事に保存でき、クラス名が消えた綺麗なHTMLが出力されましたでしょうか？

---

# you asked

「同意する」チェックボックスの設置や、MW WP Formでの必須バリデーション設定についてサポートして。

---

# gemini response

無事に表示できたようで良かったです！それでは、MW WP Formで「プライバシーポリシーに同意する」チェックボックスを設置し、チェックしないと送信できないようにする（必須バリデーション）手順を解説します。

大きく分けて **「①フォーム画面へのタグの設置」** と **「②バリデーションルールの追加」** の2ステップで完了します。

### ステップ1：フォームにチェックボックスを設置する

MW WP Formの編集画面（テキストエディタ）を開き、先ほど作成したスクロール枠のすぐ下に、チェックボックスのショートコードを追加します。

以下のコードをコピーして貼り付けてください。

```html
<div class="privacy-scroll-box" style="height: 200px; overflow-y: scroll; border: 1px solid #ccc; padding: 15px; margin-bottom: 20px;">
    [privacy_policy]
</div>

<div class="privacy-agreement" style="text-align: center; margin-bottom: 30px;">
    [mwform_checkbox name="privacy_agreement" children="プライバシーポリシーに同意する"]
</div>
```

  * **ポイント:** `name="privacy_agreement"` の部分が、このチェックボックスの「識別名」になります。次の必須設定で使うので、この名前を覚えておいてください。

-----

### ステップ2：必須（バリデーション）設定を行う

次に、チェックを入れないとエラーが出るように設定します。

1.  フォームの編集画面をそのまま**下の方へスクロール**します。
2.  **「バリデーションルールを追加」** というボタンがあるのでクリックします。
3.  新しいルールの設定枠が追加されるので、以下のように入力・チェックを入れます。

<!-- end list -->

  * **バリデーションを適用する項目:** ここに先ほど設定した `privacy_agreement` と入力します。
  * **必須:** この項目にチェック（☑️）を入れます。
  * **未入力時のメッセージ（任意）:** 空欄でも標準のエラーが出ますが、「プライバシーポリシーへの同意が必要です。」のように入力しておくと親切です。

設定できたら、忘れずに画面右上の\*\*「更新」\*\*ボタンを押してフォームを保存してください。

-----

### 確認してみましょう

実際のフォーム画面を開き、以下の動きになっているかテストしてみてください。

1.  チェックを入れずに「確認画面へ（または送信）」ボタンを押す。
2.  画面が切り替わらず、チェックボックスの近くに赤文字でエラーメッセージが表示される。
3.  チェックを入れてボタンを押すと、正常に次の画面に進む。

うまく動作しましたでしょうか？
もし、エラーメッセージの表示位置がおかしい場合や、チェックボックスのデザイン（文字の大きさなど）を調整したい場合はサポートしますので、お知らせください。