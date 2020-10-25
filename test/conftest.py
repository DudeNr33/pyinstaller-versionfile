"""
Global fixtures for test scripts.
"""

import pytest


@pytest.fixture()
def temp_version_file(tmpdir):
    return str(tmpdir / "version_file.txt")
