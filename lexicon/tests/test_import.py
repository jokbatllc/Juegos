from pathlib import Path

from django.core.management import call_command

from lexicon.models import Word


def test_import_words_command(db):
    dataset_dir = Path(__file__).resolve().parents[1] / "datasets"
    expected = sum(
        sum(1 for _ in f.open()) - 1 for f in dataset_dir.glob("*_sample.csv")
    )

    call_command("import_words")
    assert Word.objects.count() == expected

    # Running again should not duplicate entries
    call_command("import_words")
    assert Word.objects.count() == expected
