"""
Author: Andreas Finkler

Unit tests for pyinstaller_versionfile.main
"""
import os

import pytest

from pyinstaller_versionfile.main import parse_args


RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "../resources")
ACCEPTANCETEST_METADATA = os.path.join(RESOURCE_DIR, "acceptancetest_metadata.yml")
METADATA_EXT_VERSION_FILE = os.path.join(RESOURCE_DIR, "metadata_reference_to_other_file.yml")
EXT_VERSION_FILE = os.path.join(RESOURCE_DIR, "VERSION.txt")


@pytest.mark.parametrize(
    "parameter,expected_default_value", [
        ("outfile", "./version_file.txt"),
        ("version", None)
    ]
)
def test_parser_default_values(parameter, expected_default_value):
    parsed = parse_args(["in.yml"])
    assert getattr(parsed, parameter) == expected_default_value


@pytest.mark.parametrize(
    "parameter_to_check", [
        "metadata_file",
        "version",
        "outfile"
    ]
)
def test_parser_valid_parameters(parameter_to_check):
    """
    Parameters must be stored in the correct attributes of the args namespace after parsing.
    """
    parameters = dict(
        metadata_file="in.yml",
        version="123.123.123.123",
        outfile="out.txt"
    )
    args = [
        parameters["metadata_file"],
        "--version", parameters["version"],
        "--outfile", parameters["outfile"]
    ]
    parsed = parse_args(args)

    assert getattr(parsed, parameter_to_check) == parameters[parameter_to_check]


def test_parser_missing_filename():
    """
    Missing parameters must lead to a SystemExit.
    """
    args = []

    with pytest.raises(SystemExit):
        _ = parse_args(args)


def test_main_implicit_version():
    """
    The main function needs to call the correct functions on the MetaData and Writer classes.
    """


def test_main_explicit_version():
    """
    The main function needs to call the correct functions on the MetaData and Writer classes and overwrite the
    version given in the metadata file.
    """
