"""
Author: Andreas Finkler

Unit tests for pyinstaller_versionfile.main
"""
import pytest

from pyinstaller_versionfile.__main__ import parse_args_create_version_file


@pytest.mark.parametrize(
    "parameter,expected_default_value", [
        ("outfile", "./version_file.txt"),
        ("version", None)
    ]
)
def test_parser_default_values(parameter, expected_default_value):
    parsed = parse_args_create_version_file(["in.yml"])
    assert getattr(parsed, parameter) == expected_default_value


@pytest.mark.parametrize(
    "parameter_to_check", [
        "metadata_source",
        "version",
        "outfile"
    ]
)
def test_parser_valid_parameters(parameter_to_check):
    """
    Parameters must be stored in the correct attributes of the args namespace after parsing.
    """
    parameters = dict(
        metadata_source="in.yml",
        version="123.123.123.123",
        outfile="out.txt"
    )
    args = [
        parameters["metadata_source"],
        "--version", parameters["version"],
        "--outfile", parameters["outfile"]
    ]
    parsed = parse_args_create_version_file(args)

    assert getattr(parsed, parameter_to_check) == parameters[parameter_to_check]


def test_parser_missing_filename():
    """
    Missing parameters must lead to a SystemExit.
    """
    args = []

    with pytest.raises(SystemExit):
        _ = parse_args_create_version_file(args)
