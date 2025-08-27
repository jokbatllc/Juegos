import pytest
from django.conf import settings
from pytest_django.fixtures import django_db_setup  # noqa: F401


@pytest.fixture
def tmp_media_dir(tmp_path, settings):
    old_media_root = settings.MEDIA_ROOT
    settings.MEDIA_ROOT = tmp_path
    yield tmp_path
    settings.MEDIA_ROOT = old_media_root
