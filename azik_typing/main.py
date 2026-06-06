"""Main entry point for AZIK typing practice."""
import curses
import random
import sys
from collections import defaultdict
from pathlib import Path

from .azik_table import reading_to_strokes


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
    # pair 1: dim grey for untyped strokes
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    # pair 2: bright white for typed strokes
    curses.init_pair(2, curses.COLOR_WHITE, -1)
    # pair 3: status bar
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # pair 4: Japanese display text
    curses.init_pair(4, curses.COLOR_CYAN, -1)

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

        segments = reading_to_strokes(reading)
        full_strokes = "".join(stroke for _, stroke in segments)
        if not full_strokes:
            continue

        typed_count = 0

        while typed_count < len(full_strokes):
            h, w = stdscr.getmaxyx()
            stdscr.erase()

            # Line 1: Japanese / display text
            stdscr.addstr(1, 0, display[: w - 1], curses.color_pair(4))

            # Line 2: AZIK strokes — typed part bright, rest dim
            typed_part = full_strokes[:typed_count]
            remaining = full_strokes[typed_count:]
            col = 0
            if typed_part:
                stdscr.addstr(2, col, typed_part[: w - 1], curses.color_pair(2))
                col += len(typed_part)
            if remaining and col < w - 1:
                stdscr.addstr(
                    2, col, remaining[: w - 1 - col],
                    curses.color_pair(1) | curses.A_DIM,
                )

            # Status bar on last line
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

            if 32 <= ch <= 126:  # printable ASCII
                char = chr(ch)
                if char == full_strokes[typed_count]:
                    typed_count += 1
                else:
                    curses.beep()
                    # Record the miss against the current stroke segment
                    pos = 0
                    for _, stroke in segments:
                        end = pos + len(stroke)
                        if pos <= typed_count < end:
                            miss_counts[stroke] += 1
                            break
                        pos = end
                    total_misses += 1

        # Sentence cleared
        cleared += 1
        h, w = stdscr.getmaxyx()
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
    args = parser.parse_args(argv)

    if args.sentences:
        sentences_path = args.sentences
    else:
        sentences_path = find_default_sentences()

    sentences = load_sentences(sentences_path)
    if not sentences:
        print("No sentences found.", file=sys.stderr)
        sys.exit(1)

    result = curses.wrapper(run_typing, sentences)
    if result is None:
        result = (0, 0, {})

    show_results(*result)
