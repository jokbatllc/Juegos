"""Utility script to generate large word datasets per language.

Creates CSV files with 10,000 synthetic words for Spanish, English,
French and German. Each file has three columns: ``id``, ``word`` and
``language``. Files are written under ``datasets/`` and overwritten on each
run.
"""

from __future__ import annotations

import csv
from pathlib import Path

# Number of words per language
COUNT = 10_000

# Language names and a few sample base words to seed the dataset
LANG_CONFIG = {
    "es": ["gato", "perro", "casa", "libro", "coche"],
    "en": ["cat", "dog", "house", "book", "car"],
    "fr": ["chat", "chien", "maison", "livre", "voiture"],
    "de": ["katze", "hund", "haus", "buch", "auto"],
}

DATASET_DIR = Path(__file__).resolve().parent / "datasets"


def generate_words(lang: str, samples: list[str]):
    """Yield ``(id, word, language)`` tuples for the given language."""
    for i in range(1, COUNT + 1):
        if i <= len(samples):
            word = samples[i - 1]
        else:
            word = f"{lang}_word_{i:05d}"
        yield i, word, lang


def main() -> None:
    DATASET_DIR.mkdir(parents=True, exist_ok=True)

    for lang, samples in LANG_CONFIG.items():
        file_path = DATASET_DIR / f"{lang}_words.csv"
        with file_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["id", "word", "language"])
            writer.writerows(generate_words(lang, samples))
        print(f"Wrote {COUNT} words to {file_path}")


if __name__ == "__main__":
    main()
