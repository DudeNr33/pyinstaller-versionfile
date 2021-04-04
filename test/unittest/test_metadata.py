"""
Author: Andreas Finkler

Unit tests for pyinstaller_versionfile.metadata
"""

import pytest

pytestmark = pytest.mark.skip("Work in Progress")


def test_load_valid_file():
    """
    Loading a valid and complete file should succeed and the values should be returned correctly by the to_dict method.
    """
    assert False


def test_load_incomplete_file_raises_ioerror():
    """
    Loading an incomplete file (cut short at the end) shall raise an IOError.
    """
    assert False


def test_load_not_a_yaml_file_raises_usageerror():
    """
    Loading a file which is not a valid YAML file shall raise an UsageError.
    """
    assert False


def test_load_extra_parameters_are_ignored():
    """
    Any extra parameters given in the YAML file shall be silently ignored.
    """
    assert False


def test_load_directory_passed_raises_usageerror():
    """
    If a directory name instead of a filename is given, an UsageError shall be raised.
    """
    assert False


def test_load_file_does_not_exist_raises_usageerror():
    """
    If the specified file does not exist, an UsageError shall be raised.
    """
    assert False


def test_load_missing_parameters_are_given_default_values():
    """
    It is OK to leave out any parameter in the YAML file.
    In this case, an (empty) default value will be set.
    """
    assert False


def test_load_external_version_from_file():
    """
    The 'Version' parameter can specify a filename instead of a version string.
    This filepath is seen as relative to the metadata file.
    In this case the version must be read from the file provided.
    """
    assert False


def test_validate_all_parameters_ok():
    """
    If all parameters are valid than the validation should simply return.
    """
    assert False


@pytest.mark.parametrize(
    "attr,value",
    [
        ("version", "1.2.3.4.5"),  # "Version too long"
        ("version", "./thisfiledoesnotexist.yml"),  # "Non-existant version file"
        ("version", "1.2.3-rc0"),  # "Wrong version syntax 1"
        ("version", "abc9.2.1"),  # "Wrong version syntax 2"
    ]
)
def test_validate_invalid_values_raise_usageerror(attr, value):
    """
    If an invalid value is given, an UsageError must be raised.
    """
    assert False


def test_sanitize_correct_values_are_not_altered():
    """
    Values which are already good to use remain untouched.
    """
    assert False


def test_sanitize_too_short_version_will_be_filled_with_zeros():
    """
    PyInstaller expects a version with exactly 4 places.
    If a shorter version is given, the lower parts will be filled with zeros.
    """
    assert False


def test_sanitize_trailing_whitespace_gets_stripped():
    """
    Trailing whitespace in any parameter will be eliminated.
    """
    assert False


def test_set_version_valid_input_overwrites_version_from_file():
    """
    It is possible to overwrite the version read from the config file.
    """
    assert False


def test_set_version_invalid_input_raises_usageerror():
    """
    If something not interpretable as valid version string is passed to set_version, a UsageError is raised.
    """
    assert False
