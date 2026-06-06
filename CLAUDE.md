# azik-typing

SKK/AZIKタイピング練習ツール。コンソールで動作し、例文の日本語とAZIKストロークを表示してタイピングを練習する。

## 環境

```bash
python -m venv .venv
.venv/bin/pip install -e .
.venv/bin/azik-typing
```

## 構成

```
azik_typing/
  azik_table.py   AZIKかな→ストローク変換テーブルとバリアント定義
  main.py         cursesUI・入力処理・統計表示
  sentences.txt   例文ファイル（タブ区切り: 表示テキスト\t読み）
```

## azik_table.py の設計

### KANA_TO_AZIK

ひらがな列 → AZIKストロークのマッピング。greedy longest-match トライで変換する。

**サフィックス方式（AquaSKK の実動作に基づく）:**

- ん suffix は段別: `z/n`=あん、`k`=いん、`j`=うん、`d`=えん、`l`=おん
  - **母音単体（あいうえお）の後は suffix が機能しない（AquaSKK制約）**
  - おん/えん/うん/いん/あん は q fallback (oq, eq, uq, iq, aq)
  - `l` は SKK の ASCII モード切替キーのため母音直後は使えない
- 長母音 suffix: `q`=あい（A段）、`h`=うう（U段）、`w`=えい（E段）、`p`=おう（O段）
  - 同様に母音単体の後は機能しないため、おう/えい/うう も fallback (ou, ei, uu)
- っ → `;`（セミコロン）
- ん単体 → `q`

**じ行:** j形が最短（ja/ju/jo = 2打、zya/zyu/zyo = 3打）。zi/ji はどちらも有効。

**ふ行:** hu（SKK標準）と fu がバリアント。

### STROKE_VARIANTS

`{ primary_stroke: [variant1, ...] }` のマッピング。入力中にバリアントへの切替を検出するために使用。

- じ行: zi ↔ ji、ja/ju/jo ↔ zya/zyu/zyo（+ jy形）
- ふ行: hu ↔ fu、hh ↔ fh

### reading_to_strokes(reading)

`{読み}` または `{読み|送り仮名}` 形式の読み文字列をストロークリストに変換。

- `{読み}` → 先頭文字を大文字化（SKK漢字変換開始）
- `{読み|送り仮名}` → 読みの先頭と送り仮名の先頭を両方大文字化
- 戻り値: `list[tuple[str, str, bool]]` = (かな, ストローク, 漢字ブロック内フラグ)

## main.py の設計

### SegState

```python
@dataclass
class SegState:
    kana: str
    primary: str    # 画面表示の正規ストローク
    active: str     # 現在追跡中（バリアント切替で変わる）
    in_kanji: bool  # 漢字ブロック内フラグ
    done: bool
```

### 入力処理ルール

1. **正確一致** → 正解
2. **大文字許容**: `seg.active[0].isupper()` のセグメント（漢字/送り仮名の塊）内は、Shift押しっぱなしで大文字が来ても正解とみなす（母音・子音問わず）
3. **バリアント切替**: typed_so_far が STROKE_VARIANTS のいずれかの prefix と一致すれば、active をそのバリアントに変更して継続
4. **ミス**: beep + primary ストロークに記録

### 画面レイアウト

```
行1: 日本語テキスト（シアン）
行2: AZIKストローク（白=入力済み、白背景ハイライト=次の1文字、グレー=未入力）
最終行: ステータスバー
```

## sentences.txt の書き方

```
# コメント
表示テキスト[TAB]{読み}のように{か|き}ます
ひらがなのみ
```

- `{読み}` = 漢字（先頭Shift必須）
- `{読み|送り仮名}` = 送り仮名あり（読みの頭と送り仮名の頭が両方Shift）

## 注意事項

- Python 3.10+ 必須（`list[tuple[str, str, bool]]` 等の型ヒント）
- curses を使用。macOS/Linux のみ対応
- AquaSKK での動作確認済み。他のSKK実装では suffix の挙動が異なる場合がある
