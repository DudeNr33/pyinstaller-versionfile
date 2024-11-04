"""
Global fixtures for test scripts.
"""

from pathlib import Path
import pytest


@pytest.fixture()
def temp_version_file(tmp_path: Path) -> Path:
    return tmp_path / "version_file.txt"
