#!/usr/bin/env python3
"""Generate synthetic word datasets for the lexicon.

The script writes a CSV with columns ``id,word,language``.  It is useful for
creating large datasets locally without committing them to git.

Examples
--------
    python scripts/generate_dataset.py --lang es --size 10000
    python scripts/generate_dataset.py --lang en --size 5000 --output my.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

LANGS = {"es", "en", "fr", "de"}
MAX_SIZE = 50_000


def generate_words(lang: str, size: int):
    for i in range(1, size + 1):
        yield i, f"{lang}_word_{i}", lang


def write_dataset(lang: str, size: int, output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "word", "language"])
        writer.writerows(generate_words(lang, size))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic dataset")
    parser.add_argument("--lang", required=True, help="Language code (es,en,fr,de)")
    parser.add_argument("--size", type=int, default=10000, help="Number of words")
    parser.add_argument("--output", help="Output CSV path")
    args = parser.parse_args()

    lang = args.lang.lower()
    if lang not in LANGS:
        parser.error(f"Unsupported language: {args.lang}")
    if args.size > MAX_SIZE:
        parser.error(f"size must be <= {MAX_SIZE}")

    output = (
        Path(args.output)
        if args.output
        else Path(__file__).resolve().parent.parent
        / "lexicon"
        / "datasets"
        / f"auto_{lang}_{args.size}.csv"
    )

    path = write_dataset(lang, args.size, output)
    print(f"Dataset written to {path}")


if __name__ == "__main__":
    main()
