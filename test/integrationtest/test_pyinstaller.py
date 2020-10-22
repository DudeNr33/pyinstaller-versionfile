import os
import subprocess
import sys

import pytest
import yaml

from pyinstaller_versionfile.create_version_file import MetaData

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "../resources")
ACCEPTANCETEST_METADATA = os.path.join(RESOURCE_DIR, "acceptancetest_metadata.yml")
TEST_APP_PY_FILE = os.path.join(RESOURCE_DIR, "testapp.py")
TEST_APP_SPEC_FILE = os.path.join(RESOURCE_DIR, "testapp.spec")


@pytest.mark.skipif(
    not sys.platform.startswith("win")
    or os.environ.get("includeE2E", "False") != "True",
    reason="Long running test, only possible on windows OS."
)
def test_end2end_exe_generation(temp_dir, temp_version_file):
    """
    Checks if pyinstaller is able to interpret the generated version file and if the generated EXE has the correct
    version info.
    Other attributes are not checked for.
    """
    with open(ACCEPTANCETEST_METADATA) as infile:
        metadata = yaml.load(infile, Loader=yaml.CLoader)
    expected_version = metadata["Version"]
    MetaData(ACCEPTANCETEST_METADATA).create_version_file(temp_version_file)
    build_dir = os.path.join(temp_dir, "build")
    out_dir = os.path.join(temp_dir, "dist")
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
    from win32api import GetFileVersionInfo, LOWORD, HIWORD
    try:
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return "{}.{}.{}.{}".format(HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls))
    except:  # noqa
        return None
