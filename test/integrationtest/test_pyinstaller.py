"""
Integration tests for interaction with PyInstaller.
"""

import os
import subprocess
import sys

import pytest
import yaml
try:
    from unittest import mock
except ImportError:
    import mock

from pyinstaller_versionfile.__main__ import main

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "../resources")
ACCEPTANCETEST_METADATA = os.path.join(RESOURCE_DIR, "acceptancetest_metadata.yml")
TEST_APP_PY_FILE = os.path.join(RESOURCE_DIR, "testapp.py")
TEST_APP_SPEC_FILE = os.path.join(RESOURCE_DIR, "testapp.spec")


@pytest.mark.skipif(
    not sys.platform.startswith("win")
    or os.environ.get("includeE2E", "False").lower() != "true",
    reason="Long running test, only possible on windows OS."
)
def test_end2end_exe_generation(tmpdir, temp_version_file):
    """
    Checks if pyinstaller is able to interpret the generated version file and if the generated EXE has the correct
    version info.
    Other attributes are not checked for.
    """
    with open(ACCEPTANCETEST_METADATA) as infile:
        metadata = yaml.load(infile, Loader=yaml.CLoader)
    expected_version = metadata["Version"]
    args = mock.Mock()
    args.metadata_file = ACCEPTANCETEST_METADATA
    args.outfile = temp_version_file
    args.version = False
    main(args)
    build_dir = os.path.join(tmpdir, "build")
    out_dir = os.path.join(tmpdir, "dist")
    returncode = subprocess.call(
        [
            "pyinstaller",
            "--workpath", build_dir,
            "--distpath", out_dir,
            "--onefile",
            "--version-file", temp_version_file,
            TEST_APP_PY_FILE
        ]
    )
    assert returncode == 0
    file_version = get_version_number(os.path.join(out_dir, "testapp.exe"))
    assert expected_version == file_version


def get_version_number(filename):
    # pylint: disable=no-name-in-module, import-outside-toplevel, import-error
    from win32api import GetFileVersionInfo, LOWORD, HIWORD
    try:
        info = GetFileVersionInfo(filename, "\\")
        file_version_ms = info['FileVersionMS']
        file_version_ls = info['FileVersionLS']
        return "{}.{}.{}.{}".format(
            HIWORD(file_version_ms),
            LOWORD(file_version_ms),
            HIWORD(file_version_ls),
            LOWORD(file_version_ls),
        )
    except Exception:  # pylint: disable=broad-except
        return None
