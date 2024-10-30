"""
Integration tests for the command line utility provided by pyinstaller-versionfile.
"""

import os
import subprocess
from pathlib import Path

from pytest import MonkeyPatch

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "../resources")
ACCEPTANCETEST_METADATA = os.path.join(RESOURCE_DIR, "acceptancetest_metadata.yml")


def test_end2end_version_file_creation(temp_version_file: Path):
    returncode = subprocess.call(
        " ".join([
            "create-version-file",
            ACCEPTANCETEST_METADATA,
            "--outfile",
            str(temp_version_file.resolve()),
            "--version",
            "0.8.1.5",
        ]),
        shell=True,
    )
    assert returncode == 0
    assert temp_version_file.is_file()


def test_end2end_pyivf_make_version_from_yaml(temp_version_file):
    returncode = subprocess.call(
        " ".join([
            "pyivf-make_version",
            "--source-format",
            "yaml",
            "--metadata-source",
            ACCEPTANCETEST_METADATA,
            "--outfile",
            str(temp_version_file),
            "--version",
            "0.8.1.5",
        ]),
        shell=True,
    )
    assert returncode == 0
    assert os.path.isfile(temp_version_file)
    contents = temp_version_file.read_text(encoding="utf8")
    assert "filevers=(0,8,1,5)," in contents
    assert "prodvers=(0,8,1,5)," in contents
    assert "u'CompanyName', u'My Imaginary Company'" in contents
    assert "u'FileDescription', u'Acceptance Test'" in contents
    assert "u'FileVersion', u'0.8.1.5'" in contents
    assert "u'InternalName', u'Internal Acceptance Test'" in contents
    assert "u'LegalCopyright', u'© My Imaginary Company. All rights reserved.'" in contents
    assert "u'OriginalFilename', u'acceptancetest_metadata'" in contents
    assert "u'ProductName', u'Acceptance Test Unit Test'" in contents
    assert "u'ProductVersion', u'0.8.1.5'" in contents

def test_end2end_pyivf_make_version_all_default(monkeypatch: MonkeyPatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    returncode = subprocess.call("pyivf-make_version", shell=True)
    assert returncode == 0
    output_file = tmp_path / "version_file.txt"
    assert output_file.is_file()
    contents = output_file.read_text(encoding="utf8")
    assert "filevers=(0,0,0,0)," in contents
    assert "prodvers=(0,0,0,0)," in contents
    assert "u'CompanyName', u''" in contents
    assert "u'FileDescription', u''" in contents
    assert "u'FileVersion', u'0.0.0.0'" in contents
    assert "u'InternalName', u''" in contents
    assert "u'LegalCopyright', u''" in contents
    assert "u'OriginalFilename', u''" in contents
    assert "u'ProductName', u''" in contents
    assert "u'ProductVersion', u'0.0.0.0'" in contents

def test_end2end_pyivf_make_version_all_from_command_line(tmp_path: Path, temp_version_file: Path):
    returncode = subprocess.call(
        " ".join([
            "pyivf-make_version",
            "--outfile",
            str(temp_version_file),
            "--version",
            "1.2.3.4",
            "--company-name",
            '"Test Company Name"',
            "--file-description",
            '"Test File Description"',
            "--internal-name",
            '"Test Internal Name"',
            "--legal-copyright",
            '"Test Legal Copyright"',
            "--original-filename",
            '"Test Original Filename"',
            "--product-name",
            '"Test Product Name"',
        ]),
        shell=True,
    )
    assert returncode == 0
    assert temp_version_file.is_file()
    contents = temp_version_file.read_text(encoding="utf8")
    assert "filevers=(1,2,3,4)," in contents
    assert "prodvers=(1,2,3,4)," in contents
    assert "u'CompanyName', u'Test Company Name'" in contents
    assert "u'FileDescription', u'Test File Description'" in contents
    assert "u'FileVersion', u'1.2.3.4'" in contents
    assert "u'InternalName', u'Test Internal Name'" in contents
    assert "u'LegalCopyright', u'Test Legal Copyright'" in contents
    assert "u'OriginalFilename', u'Test Original Filename'" in contents
    assert "u'ProductName', u'Test Product Name'" in contents
    assert "u'ProductVersion', u'1.2.3.4'" in contents

def test_end2end_pyivf_make_version_overwrite_all_from_yaml(temp_version_file: Path) -> None:
    returncode = subprocess.call(
        " ".join([
            "pyivf-make_version",
            "--source-format",
            "yaml",
            "--metadata-source",
            ACCEPTANCETEST_METADATA,
            "--outfile",
            str(temp_version_file.resolve()),
            "--version",
            "1.2.3.4",
            "--company-name",
            '"Test Company Name"',
            "--file-description",
            '"Test File Description"',
            "--internal-name",
            '"Test Internal Name"',
            "--legal-copyright",
            '"Test Legal Copyright"',
            "--original-filename",
            '"Test Original Filename"',
            "--product-name",
            '"Test Product Name"',
        ]),
        shell=True,
    )
    assert returncode == 0
    assert temp_version_file.is_file()
    contents = temp_version_file.read_text(encoding="utf8")
    assert "filevers=(1,2,3,4)," in contents
    assert "prodvers=(1,2,3,4)," in contents
    assert "u'CompanyName', u'Test Company Name'" in contents
    assert "u'FileDescription', u'Test File Description'" in contents
    assert "u'FileVersion', u'1.2.3.4'" in contents
    assert "u'InternalName', u'Test Internal Name'" in contents
    assert "u'LegalCopyright', u'Test Legal Copyright'" in contents
    assert "u'OriginalFilename', u'Test Original Filename'" in contents
    assert "u'ProductName', u'Test Product Name'" in contents
