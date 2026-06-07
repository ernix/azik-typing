# AZIK romaji-to-kana mapping
# Based on the actual AZIK specification (celclow/azik-romaji-table)
#
# Suffix system:
#   ん: z/n=あん, k=いん, j=うん, d=えん, l=おん
#   long vowel: q=あい, h=うう, w=えい, p=おう
#   っ: ; (semicolon)
#   ん standalone: q (or nn)

KANA_TO_AZIK: dict[str, str] = {
    # ===== 基本かな =====
    "あ": "a",  "い": "i",  "う": "u",  "え": "e",  "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "si", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "ti", "つ": "tu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "hu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya",             "ゆ": "yu",             "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "ゐ": "wi",             "ゑ": "we", "を": "wo",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "ざ": "za", "じ": "zi", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "だ": "da", "ぢ": "di", "づ": "du", "で": "de", "ど": "do",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    "ん": "q",

    # ===== 拗音 =====
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
    "しゃ": "xa",  "しゅ": "xu",  "しょ": "xo",   # x形が最短 (sy形より1打短い)
    "ちゃ": "tya", "ちゅ": "tyu", "ちょ": "tyo",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "ja",  "じゅ": "ju",  "じょ": "jo",   # j形が最短 (zy形より1打短い)
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",

    # ふぁ行 (fa/fi/fe/fo — 実際のAZIKテーブルより)
    "ふぁ": "fa", "ふぃ": "fi", "ふぇ": "fe", "ふぉ": "fo",

    # ===== っ =====
    "っ": ";",

    # ===== 小文字 (l prefix) =====
    "ぁ": "la", "ぃ": "li", "ぅ": "lu", "ぇ": "le", "ぉ": "lo",
    "ゃ": "lya", "ゅ": "lyu", "ょ": "lyo",

    # ===== AZIK suffix拡張 =====
    # キーボード配置に基づく設計:
    #   各母音段のかな + 隣接キー → ん or 長音
    #
    #   ん suffix (段別キー — SKKの l キーはASCIIモード切替に使われるため O段のみ対象外):
    #     A段 + z → +ん    例: kz=かん, az=あん
    #     I段 + k → +ん    例: kk=きん
    #     U段 + j → +ん    例: kj=くん
    #     E段 + d → +ん    例: kd=けん, td=てん
    #     O段      → q fallback (SKKでlはASCIIモード切替のため shortcut なし)
    #                例: おん = o+ん = oq, こん = ko+ん = koq
    #   長母音/二重母音 suffix (段別):
    #     A段 + q → +あい    例: kq=かい
    #     U段 + h → +うう    例: kh=くう
    #     E段 + w → +えい    例: kw=けい
    #     O段 + p → +おう    例: kp=こう

    # A段 + ん (z suffix)
    # 母音単体 a に続く suffix は AquaSKK では機能しない (az, aj 等)。
    # あん → a+ん = aq (q は母音後でも有効)
    # あい → a+i = "ai" (標準ローマ字 fallback、2打で同じ)
    "かん": "kz", "かい": "kq",
    "さん": "sz", "さい": "sq",
    "たん": "tz", "たい": "tq",
    "なん": "nz", "ない": "nq",
    "はん": "hz", "はい": "hq",
    "まん": "mz", "まい": "mq",
    "らん": "rz", "らい": "rq",
    "がん": "gz", "がい": "gq",
    "ざん": "zz", "ざい": "zq",
    "だん": "dz", "だい": "dq",
    "ばん": "bz", "ばい": "bq",
    "ぱん": "pz", "ぱい": "pq",
    "やん": "yz", "やい": "yq",
    "わん": "wz", "わい": "wq",

    # I段 + ん (k suffix)
    # 「いん」は i(母音)+k → 機能しないため q fallback (iq)。
    "きん": "kk", "しん": "sk", "ちん": "tk",
    "にん": "nk", "ひん": "hk", "みん": "mk",
    "りん": "rk", "ぎん": "gk", "じん": "zk",
    "びん": "bk", "ぴん": "pk",

    # U段 + ん (j suffix) / +うう長音 (h suffix)
    # 「うん」は u(母音)+j → 機能しないため q fallback (uq)。
    # 「うう」は u(母音)+h → 機能しないため uu fallback。
    "くん": "kj", "くう": "kh",
    "すん": "sj", "すう": "sh",
    "つん": "tj", "つう": "th",
    "ぬん": "nj", "ぬう": "nh",
    "ふん": "hj", "ふう": "hh",
    "むん": "mj", "むう": "mh",
    "るん": "rj", "るう": "rh",
    "ぐん": "gj", "ぐう": "gh",
    "ずん": "zj", "ずう": "zh",
    "ぶん": "bj", "ぶう": "bh",
    "ぷん": "pj", "ぷう": "ph",
    "ゆん": "yj", "ゆう": "yh",

    # E段 + ん (d suffix) / +えい長音 (w suffix)
    # 「えん」は e(母音)+d → 機能しないため q fallback (eq)。
    # 「えい」は e(母音)+w → 機能しないため ei fallback。
    "けん": "kd", "けい": "kw",
    "せん": "sd", "せい": "sw",
    "てん": "td", "てい": "tw",
    "ねん": "nd", "ねい": "nw",
    "へん": "hd", "へい": "hw",
    "めん": "md", "めい": "mw",
    "れん": "rd", "れい": "rw",
    "げん": "gd", "げい": "gw",
    "ぜん": "zd", "ぜい": "zw",
    "でん": "dd", "でい": "dw",
    "べん": "bd", "べい": "bw",
    "ぺん": "pd", "ぺい": "pw",

    # O段 + おう長音 (p suffix) / ん (l suffix)
    # 「おん」は o(母音)+l → 機能しないため q fallback (oq)。
    # 「おう」は o(母音)+p → 機能しないため ou fallback。
    "こん": "kl", "こう": "kp",
    "そん": "sl", "そう": "sp",
    "とん": "tl", "とう": "tp",
    "のん": "nl", "のう": "np",
    "ほん": "hl", "ほう": "hp",
    "もん": "ml", "もう": "mp",
    "ろん": "rl", "ろう": "rp",
    "ごん": "gl", "ごう": "gp",
    "ぞん": "zl", "ぞう": "zp",
    "どん": "dl", "どう": "dp",
    "ぼん": "bl", "ぼう": "bp",
    "ぽん": "pl", "ぽう": "pp",
    "よん": "yl", "よう": "yp",

    # 拗音 + suffix
    "きょう": "kyp", "きょん": "kyl", "きゅん": "kyj", "きゅう": "kyh", "きゃん": "kyz", "きゃい": "kyq",
    "しょう": "xp",  "しょん": "xl",  "しゅん": "xj",  "しゅう": "xh",  "しゃん": "xz",  "しゃい": "xq",
    "ちょう": "typ", "ちょん": "tyl", "ちゅん": "tyj", "ちゅう": "tyh", "ちゃん": "tyz", "ちゃい": "tyq",
    "にょう": "nyp", "にょん": "nyl", "にゅん": "nyj", "にゅう": "nyh", "にゃん": "nyz", "にゃい": "nyq",
    "ひょう": "hyp", "ひょん": "hyl", "ひゅん": "hyj", "ひゅう": "hyh", "ひゃん": "hyz", "ひゃい": "hyq",
    "みょう": "myp", "みょん": "myl", "みゅん": "myj", "みゅう": "myh", "みゃん": "myz", "みゃい": "myq",
    "りょう": "ryp", "りょん": "ryl", "りゅん": "ryj", "りゅう": "ryh", "りゃん": "ryz", "りゃい": "ryq",
    "ぎょう": "gyp", "ぎょん": "gyl", "ぎゅん": "gyj", "ぎゅう": "gyh", "ぎゃん": "gyz", "ぎゃい": "gyq",
    "じょう": "jp",  "じょん": "jl",  "じゅん": "jj",  "じゅう": "jh",  "じゃん": "jz",  "じゃい": "jq",
    "びょう": "byp", "びょん": "byl", "びゅん": "byj", "びゅう": "byh", "びゃん": "byz", "びゃい": "byq",
    "ぴょう": "pyp", "ぴょん": "pyl", "ぴゅん": "pyj", "ぴゅう": "pyh", "ぴゃん": "pyz", "ぴゃい": "pyq",

    # ===== 子音連続ショートカット (実際のAZIKテーブルより) =====
    "こと": "kt", "した": "st", "たち": "tt", "ひと": "ht", "わた": "wt",
    "もの": "mn", "ます": "ms", "です": "ds",
    "かも": "km", "ため": "tm", "でも": "dm", "また": "mt",
    "から": "kr", "する": "sr", "たら": "tr", "なる": "nr",
    "よる": "yr", "られ": "rr", "ざる": "zr",
    "たび": "tb", "ねば": "nb", "びと": "bt",
    "がら": "gr", "ごと": "gt", "にち": "nt", "だち": "dt", "われ": "wr",

    # ===== 長音・句読点 =====
    # デフォルト: US配列では ' (アポストロフィ)
    # JIS配列では : (--jis オプション時に set_long_vowel(':') で変更)
    "ー": "'",
    "。": ".", "、": ",", "「": "[", "」": "]", "・": "/",
}


def build_trie(table: dict[str, str]) -> dict:
    """Build a trie from kana->stroke table for greedy longest-match."""
    trie: dict = {}
    for kana, stroke in table.items():
        node = trie
        for ch in kana:
            node = node.setdefault(ch, {})
        node["__stroke__"] = stroke
    return trie


AZIK_TRIE = build_trie(KANA_TO_AZIK)


def set_long_vowel(char: str) -> None:
    """長音符号のストロークを変更してトライを再構築する。
    US配列デフォルト: '  / JIS配列: :
    """
    global AZIK_TRIE
    KANA_TO_AZIK["ー"] = char
    AZIK_TRIE = build_trie(KANA_TO_AZIK)


def kana_to_azik(text: str) -> str:
    """Convert hiragana text to AZIK stroke sequence."""
    return "".join(s for _, s in kana_to_azik_segmented(text))


def kana_to_azik_segmented(text: str) -> list[tuple[str, str]]:
    """Convert hiragana text to list of (kana_segment, azik_stroke) pairs."""
    segments = []
    i = 0
    while i < len(text):
        node = AZIK_TRIE
        last_match_pos = -1
        last_match_stroke = None
        j = i
        while j < len(text) and text[j] in node:
            node = node[text[j]]
            j += 1
            if "__stroke__" in node:
                last_match_pos = j
                last_match_stroke = node["__stroke__"]
        if last_match_stroke is not None:
            segments.append((text[i:last_match_pos], last_match_stroke))
            i = last_match_pos
        else:
            segments.append((text[i], text[i]))
            i += 1
    return segments


def reading_to_strokes(reading: str) -> list[tuple[str, str]]:
    """Convert a reading string with optional {kanji_reading} markers to stroke pairs.

    Text inside {braces} represents a kanji/katakana word following SKK convention:
      - {reading}        : first letter uppercased (Shift at kanji start)
      - {reading|okuri}  : first letter of each part uppercased
                           (Shift at kanji start AND at okurigana start)

    Examples:
      "{きょう}はいい{てんき}ですね"  -> KyphqiTdkiDs
      "{おお|き}な"                   -> OpKina
      "{か|い}た"                     -> KqIta   (書いた)
    """
    # _KATA: カタカナ変換トリガー '[' を追加するための sentinel
    _KATA = "\x00["

    # blocks: (text, needs_shift, triggers_next)
    #   triggers_next=True: 送り仮名なしの漢字ブロック ({text} のみ)。
    #   直後のひらがな先頭文字を大文字にする — AquaSKK では Shift+子音が
    #   漢字変換を確定しつつ次の文字入力を始めるため。
    blocks: list[tuple[str, bool, bool]] = []
    i = 0
    while i < len(reading):
        if reading[i] == "{":
            close = reading.find("}", i + 1)
            if close == -1:
                blocks.append((reading[i + 1:], False, False))
                break
            inner = reading[i + 1:close]
            if "|" in inner:
                kanji_part, okuri_part = inner.split("|", 1)
                blocks.append((kanji_part, True, False))   # 読み部 (送り仮名で完結しない)
                blocks.append((okuri_part, True, False))   # 送り仮名 (次を大文字化しない)
            else:
                blocks.append((inner, True, True))          # 単純漢字ブロック → 次を大文字化
            i = close + 1
        elif reading[i] == "[":
            # カタカナ語: [よみ] → 先頭大文字(Shift) + 読み + [ (カタカナ変換)
            close = reading.find("]", i + 1)
            if close == -1:
                blocks.append((reading[i + 1:], True, False))
                break
            blocks.append((reading[i + 1:close], True, False))
            blocks.append((_KATA, False, False))   # カタカナ変換トリガー
            i = close + 1
        else:
            j_brace   = reading.find("{", i)
            j_bracket = reading.find("[", i)
            if j_brace == -1:
                j = j_bracket
            elif j_bracket == -1:
                j = j_brace
            else:
                j = min(j_brace, j_bracket)
            chunk = reading[i:] if j == -1 else reading[i:j]
            if chunk:
                blocks.append((chunk, False, False))
            i = len(reading) if j == -1 else j

    # (kana, stroke, in_kanji_block) — in_kanji_block はShift許容の判定に使う
    result: list[tuple[str, str, bool]] = []
    for text, needs_shift, triggers_next in blocks:
        if text == _KATA:
            result.append(("", "[", False))   # カタカナ変換トリガーキー
            continue
        segs = kana_to_azik_segmented(text)
        for k, (kana, stroke) in enumerate(segs):
            if needs_shift and k == 0:
                if stroke and stroke[0].isalpha():
                    stroke = stroke[0].upper() + stroke[1:]
                elif stroke == ";":
                    # っ が送り仮名変換トリガーの場合: Shift+; = : (US配列)
                    stroke = ":"
            result.append((kana, stroke, needs_shift))
        if triggers_next:
            result.append(("", " ", False))   # SKK変換確定スペース
    return result


# ---------------------------------------------------------------------------
# バリアント定義
# 同じかなを異なるストロークで入力できる場合のマッピング。
# キー: 正規ストローク (小文字), 値: 受け付ける代替ストロークのリスト
# ---------------------------------------------------------------------------
STROKE_VARIANTS: dict[str, list[str]] = {
    # じ (zi/ji は同打鍵数)
    "zi": ["ji"],
    "zk": ["jk"],   # じん
    # じゃ/じゅ/じょ: j形(2打)が最短、zy形・jy形(3打)が代替
    "ja":  ["zya", "jya"],  # じゃ
    "ju":  ["zyu", "jyu"],  # じゅ
    "jo":  ["zyo", "jyo"],  # じょ
    "jp":  ["zyp", "jyp"],  # じょう
    "jl":  ["zyl", "jyl"],  # じょん
    "jj":  ["zyj", "jyj"],  # じゅん
    "jh":  ["zyh", "jyh"],  # じゅう
    "jz":  ["zyz", "jyz"],  # じゃん
    "jq":  ["zyq", "jyq"],  # じゃい
    # し行: x形(2打)が最短、sy形(3打)が代替
    "xa":  ["sya"],  # しゃ
    "xu":  ["syu"],  # しゅ
    "xo":  ["syo"],  # しょ
    "xp":  ["syp"],  # しょう
    "xl":  ["syl"],  # しょん
    "xj":  ["syj"],  # しゅん
    "xh":  ["syh"],  # しゅう
    "xz":  ["syz"],  # しゃん
    "xq":  ["syq"],  # しゃい
    # ふ行: hu形(SKK標準)と fu形 はどちらも有効
    "hu":  ["fu"],   # ふ
    "hj":  ["fj"],   # ふん
    "hh":  ["fh"],   # ふう
}


def get_variants(stroke: str) -> list[str]:
    """正規ストロークに対応する代替ストロークの一覧を返す。

    SKK大文字（漢字変換開始）に対応するため、先頭が大文字の場合は
    小文字で検索して結果を同じ大文字化パターンで返す。
    """
    if stroke and stroke[0].isupper():
        lower_variants = STROKE_VARIANTS.get(stroke[0].lower() + stroke[1:], [])
        return [v[0].upper() + v[1:] for v in lower_variants]
    return STROKE_VARIANTS.get(stroke, [])
