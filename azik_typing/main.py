"""Main entry point for AZIK typing practice."""
import curses
import random
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .azik_table import get_variants, reading_to_strokes, set_long_vowel


@dataclass
class SegState:
    kana: str
    primary: str          # 正規AZIKストローク（画面表示の初期値）
    active: str           # 現在追跡中のストローク（バリアントに切替わることがある）
    in_kanji: bool = False  # 漢字ブロック内 → Shift押しっぱなしを許容
    done: bool = False


def _build_display(states: list[SegState], seg_idx: int, pos_in_seg: int) -> tuple[str, int]:
    """画面表示用のストローク文字列と入力済み文字数を返す。

    - 完了セグメント: 実際に入力されたストローク（バリアント含む）
    - 現在セグメント: active ストローク（バリアントに切替わっていれば更新済み）
    - 未来セグメント: primary ストローク（まだ表示は変えない）
    """
    parts = [
        st.active if i <= seg_idx else st.primary
        for i, st in enumerate(states)
    ]
    typed_count = sum(len(st.active) for st in states[:seg_idx]) + pos_in_seg
    return "".join(parts), typed_count


def load_sentences(path: Path) -> list[tuple[str, str]]:
    """Load sentences as (display_text, reading) tuples.

    File format: one sentence per line.
    Lines with a tab are treated as "display\\treading".
    Lines without a tab are used as both display and reading.
    """
    pairs = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "\t" in line:
            display, reading = line.split("\t", 1)
            pairs.append((display.strip(), reading.strip()))
        else:
            pairs.append((line, line))
    return pairs


def find_default_sentences() -> Path:
    here = Path(__file__).parent
    candidate = here / "sentences.txt"
    if candidate.exists():
        return candidate
    raise FileNotFoundError("sentences.txt not found. Use --sentences <path>.")


def run_typing(
    stdscr: "curses._CursesWindow",
    sentences: list[tuple[str, str]],
) -> tuple[int, int, dict[str, int]]:
    curses.curs_set(1)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)   # dim: 未入力ストローク
    curses.init_pair(2, curses.COLOR_WHITE, -1)   # bright: 入力済みストローク
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # ステータスバー
    curses.init_pair(4, curses.COLOR_CYAN, -1)    # 日本語テキスト
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)  # 次に打つ文字のハイライト

    cleared = 0
    total_misses = 0
    miss_counts: dict[str, int] = defaultdict(int)

    order = list(range(len(sentences)))
    random.shuffle(order)
    idx = 0

    while True:
        if idx >= len(order):
            random.shuffle(order)
            idx = 0
        display, reading = sentences[order[idx]]
        idx += 1

        raw_segs = reading_to_strokes(reading)
        if not raw_segs:
            continue

        # セグメントごとに状態を管理する
        states = [SegState(kana=k, primary=s, active=s, in_kanji=ik)
                  for k, s, ik in raw_segs]
        seg_idx = 0
        pos_in_seg = 0
        in_miss = False  # ミス直後フラグ: 正解が来るまで追加ミスをカウントしない

        while seg_idx < len(states):
            h, w = stdscr.getmaxyx()
            stdscr.erase()

            full_strokes, typed_count = _build_display(states, seg_idx, pos_in_seg)

            # 日本語テキスト
            stdscr.addstr(1, 0, display[: w - 1], curses.color_pair(4))

            # AZIKストローク（入力済み=白, 次の1文字=ハイライト, 残り=グレー）
            typed_part = full_strokes[:typed_count]
            next_char  = full_strokes[typed_count:typed_count + 1]
            remaining  = full_strokes[typed_count + 1:]
            col = 0
            if typed_part and col < w - 1:
                stdscr.addstr(2, col, typed_part[: w - 1], curses.color_pair(2))
                col += len(typed_part)
            if next_char and col < w - 1:
                stdscr.addstr(2, col, next_char, curses.color_pair(5))
                col += 1
            if remaining and col < w - 1:
                stdscr.addstr(
                    2, col, remaining[: w - 1 - col],
                    curses.color_pair(1) | curses.A_DIM,
                )

            status = f" Cleared: {cleared}  Misses: {total_misses}  (Ctrl-C to quit) "
            stdscr.addstr(h - 1, 0, status[: w - 1], curses.color_pair(3))
            stdscr.move(2, min(typed_count, w - 2))
            stdscr.refresh()

            try:
                ch = stdscr.getch()
            except KeyboardInterrupt:
                return cleared, total_misses, dict(miss_counts)

            if ch == 3:  # Ctrl-C
                return cleared, total_misses, dict(miss_counts)

            if not (32 <= ch <= 126):
                continue

            seg = states[seg_idx]
            char = chr(ch)
            expected = seg.active[pos_in_seg]
            # 大文字始まりのセグメント内（= Shift で開始する漢字/送り仮名の塊）は、
            # 母音・子音を問わず大文字入力を許容する（Shift押しっぱなし対応）。
            # 別セグメント（ひらがな部分や次の漢字塊）には適用しない。
            in_kanji = seg.active[0].isupper()

            def _matches(c: str, exp: str) -> bool:
                return c == exp or (
                    in_kanji
                    and exp.islower()
                    and c == exp.upper()
                )

            if _matches(char, expected):
                # 正解: 次の文字へ（ミス状態も解除）
                in_miss = False
                pos_in_seg += 1
                if pos_in_seg == len(seg.active):
                    seg.done = True
                    seg_idx += 1
                    pos_in_seg = 0
            else:
                # 不正解: バリアントを確認する
                # これまでに入力した文字 + 今押したキーがいずれかのバリアントの
                # 先頭部分と一致するか調べる
                typed_so_far = seg.active[:pos_in_seg] + char
                matched = next(
                    (v for v in get_variants(seg.primary)
                     if v.startswith(typed_so_far)),
                    None,
                )

                if matched is not None:
                    # バリアントに切替え: 表示を更新して処理継続
                    in_miss = False
                    seg.active = matched
                    pos_in_seg = len(typed_so_far)
                    if pos_in_seg == len(seg.active):
                        seg.done = True
                        seg_idx += 1
                        pos_in_seg = 0
                else:
                    # ミスタイプ: 最初の1回だけ記録（連打は無視）
                    curses.beep()
                    if not in_miss:
                        miss_counts[seg.primary] += 1
                        total_misses += 1
                        in_miss = True

        # 例文クリア
        cleared += 1
        h, w = stdscr.getmaxyx()
        full_strokes, _ = _build_display(states, len(states), 0)
        stdscr.erase()
        stdscr.addstr(1, 0, display[: w - 1], curses.color_pair(4))
        stdscr.addstr(2, 0, full_strokes[: w - 1], curses.color_pair(2))
        status = f" Cleared: {cleared}  Misses: {total_misses}  (Ctrl-C to quit) "
        stdscr.addstr(h - 1, 0, status[: w - 1], curses.color_pair(3))
        stdscr.refresh()
        curses.napms(500)


def show_results(cleared: int, misses: int, miss_counts: dict[str, int]) -> None:
    print("\n" + "=" * 40)
    print(f"  Cleared sentences : {cleared}")
    print(f"  Total misses      : {misses}")
    print()
    if miss_counts:
        ranked = sorted(miss_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        print("  Top mistyped strokes:")
        for rank, (stroke, count) in enumerate(ranked, 1):
            print(f"    {rank}. [{stroke}]  ×{count}")
    else:
        print("  No misses — perfect!")
    print("=" * 40 + "\n")


def main(argv: list[str] | None = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="AZIK typing practice")
    parser.add_argument(
        "--sentences", "-s",
        type=Path,
        default=None,
        help="Path to sentences text file (one sentence per line)",
    )
    parser.add_argument(
        "--jis",
        action="store_true",
        help="JIS配列モード: 長音符号を ' の代わりに : にする",
    )
    args = parser.parse_args(argv)

    if args.jis:
        set_long_vowel(":")

    sentences_path = args.sentences or find_default_sentences()
    sentences = load_sentences(sentences_path)
    if not sentences:
        print("No sentences found.", file=sys.stderr)
        sys.exit(1)

    result = curses.wrapper(run_typing, sentences)
    show_results(*(result or (0, 0, {})))
