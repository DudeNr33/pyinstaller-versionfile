"""
Author: Andreas Finkler

Unit tests for the functional API of pyinstaller_versionfile.
"""
from pathlib import Path

import pyinstaller_versionfile

TEST_DATA = Path(__file__).parent.parent / "resources"
INPUT_METADATA_FILE = TEST_DATA / "acceptancetest_metadata.yml"
EXPECTED_VERSIONFILE = TEST_DATA / "acceptancetest_expected_versionfile.txt"


def test_create_versionfile(tmpdir):
    """
    Creation of a versionfile must be possible without having to use an input file.
    """
    output_file = tmpdir / "versionfile.txt"
    pyinstaller_versionfile.create_versionfile(
        output_file=output_file,
        version="4.7.1.1",
        company_name="My Imaginary Company",
        file_description="Acceptance Test",
        internal_name="Internal Acceptance Test",
        legal_copyright="© My Imaginary Company. All rights reserved.",
        original_filename="acceptancetest_metadata",
        product_name="Acceptance Test Unit Test",
        translations=[0, 1252, 1031, 1200],
    )

    assert output_file.read_text(encoding="utf8") == EXPECTED_VERSIONFILE.read_text(
        encoding="utf8"
    )


def test_create_versionfile_from_input_file(tmpdir):
    """
    Creation of a versionfile must be possible by passing in an input file.
    """
    output_file = tmpdir / "versionfile.txt"
    pyinstaller_versionfile.create_versionfile_from_input_file(
        output_file=output_file, input_file=INPUT_METADATA_FILE
    )

    assert output_file.read_text(encoding="utf8") == EXPECTED_VERSIONFILE.read_text(
        encoding="utf8"
    )


def test_create_versionfile_from_input_file_overwrite_version(tmpdir):
    """
    If an explicit version was specified, it must take precedence over the information given in the file.
    """
    output_file = tmpdir / "versionfile.txt"
    pyinstaller_versionfile.create_versionfile_from_input_file(
        output_file=output_file, input_file=INPUT_METADATA_FILE, version="9.8.7.6"
    )

    assert "filevers=(9,8,7,6)" in output_file.read_text(encoding="utf8")
