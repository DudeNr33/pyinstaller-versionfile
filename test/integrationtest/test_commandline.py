"""
Integration tests for the command line utility provided by pyinstaller-versionfile.
"""

import os
import subprocess

import pytest

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "../resources")
ACCEPTANCETEST_METADATA = os.path.join(RESOURCE_DIR, "acceptancetest_metadata.yml")


@pytest.mark.skipif(os.environ.get("includeE2E", "False").lower() != "true", reason="Only possbile in tox environment.")
def test_end2end_version_file_creation(temp_version_file):
    returncode = subprocess.call(
        [
            "create-version-file",
            ACCEPTANCETEST_METADATA,
            "--outfile", temp_version_file,
            "--version", "0.8.1.5"
        ]
    )
    assert returncode == 0
    assert os.path.isfile(temp_version_file)
