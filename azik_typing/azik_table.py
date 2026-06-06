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
    "しゃ": "sya", "しゅ": "syu", "しょ": "syo",
    "ちゃ": "tya", "ちゅ": "tyu", "ちょ": "tyo",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "zya", "じゅ": "zyu", "じょ": "zyo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",

    # ===== っ =====
    "っ": ";",

    # ===== 小文字 (l prefix) =====
    "ぁ": "la", "ぃ": "li", "ぅ": "lu", "ぇ": "le", "ぉ": "lo",
    "ゃ": "lya", "ゅ": "lyu", "ょ": "lyo",

    # ===== AZIK suffix拡張 =====
    # キーボード配置に基づく設計:
    #   各母音段のかな + 隣接キー → ん or 長音
    #
    #   A段 (あかさたなはまらがざだばぱ) + z/n → +ん, + q → +い
    #   I段 (いきしちにひみりぎじぢびぴ) + k → +ん
    #   U段 (うくすつぬふむるぐずづぶぷ) + j → +ん, + h → +う(長音)
    #   E段 (えけせてねへめれげぜでべぺ) + d → +ん, + w → +い(えい)
    #   O段 (おこそとのほもろごぞどぼぽ) + l → +ん, + p → +う(おう)

    # A段 + ん (z suffix) / +い (q suffix)
    "あん": "az", "あい": "aq",
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
    "いん": "ik",
    "きん": "kk", "しん": "sk", "ちん": "tk",
    "にん": "nk", "ひん": "hk", "みん": "mk",
    "りん": "rk", "ぎん": "gk", "じん": "zk",
    "びん": "bk", "ぴん": "pk",

    # U段 + ん (j suffix) / +う長音 (h suffix)
    "うん": "uj", "うう": "uh",
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

    # E段 + ん (d suffix) / +い長音 (w suffix, えい sound)
    "えん": "ed", "えい": "ew",
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

    # O段 + ん (l suffix) / +う長音 (p suffix, おう sound)
    "おん": "ol", "おう": "op",
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
    # きょ段 (o-suffix: p=おう, l=おん) / きゅ段 (u-suffix: j=うん, h=うう)
    # きゃ段 (a-suffix: z=あん, q=あい)
    "きょう": "kyp", "きょん": "kyl",
    "きゅん": "kyj", "きゅう": "kyh",
    "きゃん": "kyz", "きゃい": "kyq",
    "しょう": "syp", "しょん": "syl",
    "しゅん": "syj", "しゅう": "syh",
    "しゃん": "syz", "しゃい": "syq",
    "ちょう": "typ", "ちょん": "tyl",
    "ちゅん": "tyj", "ちゅう": "tyh",
    "ちゃん": "tyz", "ちゃい": "tyq",
    "にょう": "nyp", "にょん": "nyl",
    "にゅん": "nyj", "にゅう": "nyh",
    "にゃん": "nyz", "にゃい": "nyq",
    "ひょう": "hyp", "ひょん": "hyl",
    "ひゅん": "hyj", "ひゅう": "hyh",
    "ひゃん": "hyz", "ひゃい": "hyq",
    "みょう": "myp", "みょん": "myl",
    "みゅん": "myj", "みゅう": "myh",
    "みゃん": "myz", "みゃい": "myq",
    "りょう": "ryp", "りょん": "ryl",
    "りゅん": "ryj", "りゅう": "ryh",
    "りゃん": "ryz", "りゃい": "ryq",
    "ぎょう": "gyp", "ぎょん": "gyl",
    "ぎゅん": "gyj", "ぎゅう": "gyh",
    "ぎゃん": "gyz", "ぎゃい": "gyq",
    "じょう": "zyp", "じょん": "zyl",
    "じゅん": "zyj", "じゅう": "zyh",
    "じゃん": "zyz", "じゃい": "zyq",
    "びょう": "byp", "びょん": "byl",
    "びゅん": "byj", "びゅう": "byh",
    "びゃん": "byz", "びゃい": "byq",
    "ぴょう": "pyp", "ぴょん": "pyl",
    "ぴゅん": "pyj", "ぴゅう": "pyh",
    "ぴゃん": "pyz", "ぴゃい": "pyq",

    # ===== 子音連続ショートカット (実際のAZIKテーブルより) =====
    "こと": "kt", "した": "st", "たち": "tt", "ひと": "ht", "わた": "wt",
    "もの": "mn", "ます": "ms", "です": "ds",
    "かも": "km", "ため": "tm", "でも": "dm", "また": "mt",
    "から": "kr", "する": "sr", "たら": "tr", "なる": "nr",
    "よる": "yr", "られ": "rr", "ざる": "zr",
    "たび": "tb", "ねば": "nb", "びと": "bt",
    "がら": "gr", "ごと": "gt", "にち": "nt", "だち": "dt", "われ": "wr",

    # ===== 長音・句読点 =====
    "ー": "-",
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
    blocks: list[tuple[str, bool]] = []
    i = 0
    while i < len(reading):
        if reading[i] == "{":
            close = reading.find("}", i + 1)
            if close == -1:
                blocks.append((reading[i + 1:], False))
                break
            inner = reading[i + 1:close]
            if "|" in inner:
                kanji_part, okuri_part = inner.split("|", 1)
                blocks.append((kanji_part, True))
                blocks.append((okuri_part, True))
            else:
                blocks.append((inner, True))
            i = close + 1
        else:
            j = reading.find("{", i)
            chunk = reading[i:] if j == -1 else reading[i:j]
            if chunk:
                blocks.append((chunk, False))
            i = len(reading) if j == -1 else j

    result: list[tuple[str, str]] = []
    for text, needs_shift in blocks:
        segs = kana_to_azik_segmented(text)
        for k, (kana, stroke) in enumerate(segs):
            if needs_shift and k == 0 and stroke and stroke[0].isalpha():
                stroke = stroke[0].upper() + stroke[1:]
            result.append((kana, stroke))
    return result
