# Workflow 05: Style B (ピークエネルギ抽出) 実装計画

## 目標
ショート動画のスタイルBにおいて、曲の最初から順に固定で15秒切り出すのではなく、**「曲の中で最も音圧・エネルギーが高い（盛り上がっている）15秒間」** を自動算出して切り出すロジックを実装します。

## 提案する実装アプローチ: エネルギーベースのスライディングウィンドウ
FFmpeg単体では「一番数値が高い場所を探す」処理ができないため、Python側で波形データ（または音量データ）を分析し、最適な開始位置（秒数）を計算してから FFmpeg にトリミング範囲（`start=X:end=X+15`）として渡します。

### 1. 音声解析・切り出し位置の計算 (Pythonメイン)
複雑で重いライブラリ（`librosa` など）を導入しなくても、**FFmpegの `volumedetect` や `astats` フィルタ、あるいは標準の [pydub](file:///c:/Users/kuseg/%E3%82%8A%E3%82%85%E3%81%86%E3%81%8D/antigravity/05_yt_music_long/src/04_03_audio_processor.py#157-235) / `wave` ライブラリとチャンク分割** を使って簡易的に「指定秒数ごとのRMS（実効値）やラウドネス」を計算することが十分可能です。

今回は既存で使っているツールの枠組み（FFmpeg や pydub 等）を最大限活用し、シンプルに以下の計算モデルを作成します。
1. 音声ファイル全体を 1秒 ごとのチャンク（フレーム）の音量（RMSまたは振幅ベース）配列に変換。
2. 配列上で「長さ15秒」のウィンドウを1秒ずつスライドさせ、ウィンドウ内のエネルギー合計（または平均RMS）を計算。
3. 合計が最大となる開始位置 `T` (秒) を求める。

### 2. [src/05_01_short_creator.py](file:///c:/Users/kuseg/%E3%82%8A%E3%82%85%E3%81%86%E3%81%8D/antigravity/05_yt_music_long/src/05_01_short_creator.py) の改修内容
- [NEW/MODIFY] [src/05_01_short_creator.py](file:///c:/Users/kuseg/%E3%82%8A%E3%82%85%E3%81%86%E3%81%8D/antigravity/05_yt_music_long/src/05_01_short_creator.py)
  - 新機能: `find_highest_energy_window(file_path, window_duration=15)` 関数を追加します。
  - **FFmpeg `astats` の利用:** 別途重いライブラリを用意せずとも、FFmpegコマンドで0.5秒〜1秒ごとの音圧レベル（RMS）をテキストに書き出し、それをPythonで一瞬でパースしてスライディングウィンドウを計算できます。あるいは `pydub.AudioSegment` を読み込んで `.rms` を計算するのも高速でおすすめです。（プロジェクトで [pydub](file:///c:/Users/kuseg/%E3%82%8A%E3%82%85%E3%81%86%E3%81%8D/antigravity/05_yt_music_long/src/04_03_audio_processor.py#157-235) はFFmpegをラップして使用実績があるため、[pydub](file:///c:/Users/kuseg/%E3%82%8A%E3%82%85%E3%81%86%E3%81%8D/antigravity/05_yt_music_long/src/04_03_audio_processor.py#157-235) を使用予定です）。
  - **パターンの動的ロード対応:**
    Style A はこれまで通り `atrim=0:15` (曲頭から15秒) とします。
    Style B の場合は、`audio1_start = find_highest_energy_window(audio1)` と `audio2_start = find_highest_energy_window(audio2)` をそれぞれ計算します。
  - 計算結果を変数 (`a1_start`, `a2_start`) として抽出し、FFmpegの引数に当てはめます。

### 3. パターンファイル [pattern-02-zoom.md](file:///c:/Users/kuseg/%E3%82%8A%E3%82%85%E3%81%86%E3%81%8D/antigravity/05_yt_music_long/.agent/skills/05_01_short_creator/patterns/pattern-02-zoom.md) への変数注入
Style B に対して計算した開始位置を `audio_filter` 内の `atrim` に反映させるため、Python側から引数として `a1_start` と `a2_start` 文字列を渡せるようにFFmpegフィルター構造を整理します。

## メリット
- サビや盛り上がりのドロップ部分を自動で引けるため、アンビエントやEDMなどインスト楽曲でも最もおいしい15秒間をショート化できる。
- [pydub](file:///c:/Users/kuseg/%E3%82%8A%E3%82%85%E3%81%86%E3%81%8D/antigravity/05_yt_music_long/src/04_03_audio_processor.py#157-235) や既存ライブラリ・FFmpegの機能を使うため、新規に重い機械学習ライブラリ等を入れずに10秒以内でサクサク計算可能。

この手順で実装を進めてよろしいでしょうか？
