import pytest
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
@pytest.fixture
def django_settings_5_1_3():
    with open(CURRENT_DIR / "django" / "settings_5.1.3.py") as fp:
        return fp.read()

@pytest.fixture
def django_settings_5_1_3_modified():
    with open(CURRENT_DIR / "django" / "settings_5.1.3.modified.py") as fp:
        return fp.read()