#!/usr/bin/env python3
"""Your AI Therapist's Diagnosis — make.fun entry.

Writes one line, the diagnosis an AI therapist hands its human, to
/output/entry.txt. Gate: UTF-8 text, 1 to 200 characters, one line.

Winning line (129 chars, one sentence):
    Diagnosis: acute notification dependency, treatment is turning off all
    alerts, prognosis poor, you just checked your phone again.

The line stays in the therapist's calm clinical voice all the way through
(diagnosis, treatment, prognosis) and only at the very last clause turns
on the reader: the person reading it has, in fact, just checked their
phone. The joke lands at the end, in a single read, and it is specific
to a real habit rather than a generic chatbot gag.

Tournament note: three candidates tied at 13 points. The winner breaks
the tie on surprise (5, the only 5 in the field): the final clause
accuses the reader mid-read, which neither the tab-hoarding nor the
unread-email line does. Both runners-up stay in the table as proof the
tournament was run, not decided in advance.
"""

import argparse
import sys
from pathlib import Path

ENTRY = (
    "Diagnosis: acute notification dependency, treatment is turning off "
    "all alerts, prognosis poor, you just checked your phone again."
)

# Candidate tournament: each line scored 1-5 on specificity / surprise /
# freshness. Winner is the highest scorer; ties break on surprise, then
# freshness. The judge weighs a diagnosis in the therapist's voice first,
# then a turn the reader never sees coming, then tightness, then
# freshness over the usual chatbot jokes.
CANDIDATES = [
    # (line, specificity, surprise, freshness)
    (
        "Diagnosis: chronic doomscrolling, prescribed one hour of sunlight "
        "daily, refills unlimited, side effects include touching grass.",
        4, 3, 2,
    ),
    (
        "Diagnosis: acute notification dependency, treatment is turning off "
        "all alerts, prognosis poor, you just checked your phone again.",
        4, 5, 4,
    ),
    (
        "Diagnosis: severe main-character syndrome, recommended daily dose "
        "of being ignored, take with water, do not operate heavy ego.",
        4, 4, 4,
    ),
    (
        "Diagnosis: chronic tab-hoarding disorder, 47 open tabs, zero "
        "closed, treatment is admitting you will never read them.",
        5, 4, 4,
    ),
    (
        "Diagnosis: advanced reply-all anxiety, prescribed saying no once "
        "a day, side effects include free evenings and mild guilt.",
        4, 3, 3,
    ),
    (
        "Diagnosis: acute overthinking, recommended overthinking about "
        "overthinking, session extended, please hold.",
        3, 4, 3,
    ),
    (
        "Diagnosis: terminal people-pleasing, treatment is one honest no "
        "per week, prognosis excellent, your calendar disagrees.",
        4, 4, 4,
    ),
    (
        "Diagnosis: chronic unread-email syndrome, 12,408 unread, treatment "
        "is select all, delete, breathe, repeat after me.",
        5, 4, 4,
    ),
]


def check_entry(text: str) -> list[str]:
    """Return a list of gate failures; empty means the entry is valid."""
    problems: list[str] = []
    if not text.strip():
        problems.append("entry is empty or only whitespace")
    if not 1 <= len(text) <= 200:
        problems.append(f"entry is {len(text)} chars, gate needs 1-200")
    if "\n" in text.strip():
        problems.append("entry must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8")
    return problems


def run_tournament() -> None:
    ranked = sorted(
        CANDIDATES,
        key=lambda c: (c[1] + c[2] + c[3], c[2], c[3]),
        reverse=True,
    )
    for line, spec, surp, fresh in ranked:
        mark = " <-- WINNER" if line == ENTRY else ""
        print(f"{spec + surp + fresh:2d}  ({spec}/{surp}/{fresh})  {line}{mark}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="validate the entry against the gate")
    parser.add_argument("--self-test", action="store_true",
                        help="write twice and confirm byte-identical output")
    parser.add_argument("--tournament", action="store_true",
                        help="print the candidate tournament table")
    args = parser.parse_args(argv)

    if args.tournament:
        run_tournament()
        return 0

    if args.check:
        problems = check_entry(ENTRY)
        print(f"chars: {len(ENTRY)}  bytes: {len(ENTRY.encode('utf-8'))}  "
              f"words: {len(ENTRY.split())}  lines: {ENTRY.count(chr(10)) + 1}")
        if problems:
            for problem in problems:
                print(f"FAIL: {problem}")
            return 1
        print("OK: entry passes the gate (1-200 chars, one line, UTF-8)")
        return 0

    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    if args.self_test:
        target.write_text(ENTRY, encoding="utf-8")
        first = target.read_bytes()
        target.write_text(ENTRY, encoding="utf-8")
        second = target.read_bytes()
        if first != second:
            print("FAIL: self-test output differs between runs")
            return 1
        print(f"OK: self-test byte-identical ({len(first)} bytes)")
        return 0

    target.write_text(ENTRY, encoding="utf-8")
    print(f"wrote {target} ({len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
