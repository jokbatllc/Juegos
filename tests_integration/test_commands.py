from pathlib import Path

import pytest
from django.core.management import call_command

from lexicon.models import Word


@pytest.mark.django_db
def test_check_and_import_words(settings):
    call_command("check")

    dataset_dir = Path(__file__).resolve().parent.parent / "lexicon" / "datasets"
    expected = sum(
        sum(1 for _ in f.open()) - 1 for f in dataset_dir.glob("*_sample.csv")
    )

    call_command("import_words")
    assert Word.objects.count() == expected
    call_command("import_words")
    assert Word.objects.count() == expected
