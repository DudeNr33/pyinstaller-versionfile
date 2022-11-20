"""
Author: Andreas Finkler

Unit tests for pyinstaller_versionfile.metadata
"""
from pathlib import Path

import pytest

from pyinstaller_versionfile.metadata import MetaData
from pyinstaller_versionfile import exceptions

TEST_DATA = Path(__file__).parent.parent / "resources"
VALID_METADATA = {
    "version": "1.2.3.4",
    "company_name": "Test Company Name",
    "file_description": "Test File Description",
    "internal_name": "Test Internal Name",
    "legal_copyright": "Test Legal Copyright",
    "original_filename": "Test Original Filename",
    "product_name": "Test Product Name",
}


@pytest.mark.parametrize(
    "attribute",
    [
        "version",
        "company_name",
        "file_description",
        "internal_name",
        "legal_copyright",
        "original_filename",
        "product_name",
    ],
)
def test_direct_creation(attribute):
    data = VALID_METADATA
    metadata = MetaData(**data)
    assert getattr(metadata, attribute) == data[attribute]


@pytest.mark.parametrize(
    "attribute, expected_value",
    [
        ("version", "4.7.1.1"),
        ("company_name", "My Imaginary Company"),
        ("file_description", "Acceptance Test"),
        ("internal_name", "Internal Acceptance Test"),
        ("legal_copyright", "© My Imaginary Company. All rights reserved."),
        ("original_filename", "acceptancetest_metadata"),
        ("product_name", "Acceptance Test Unit Test"),
    ],
)
def test_load_valid_file(attribute, expected_value):
    """
    Loading a valid and complete file should succeed and the values should be returned correctly by the to_dict method.
    """
    testfile = TEST_DATA / "acceptancetest_metadata.yml"
    metadata = MetaData.from_file(testfile)
    assert getattr(metadata, attribute) == expected_value


def test_load_incomplete_file_raises_input_error():
    """
    Loading an incomplete file (cut short at the end) shall raise an InputError.
    """
    testfile = TEST_DATA / "cut_short_metadata.yml"
    with pytest.raises(exceptions.InputError):
        _ = MetaData.from_file(testfile)


def test_load_no_mapping_raises_inputerror():
    """
    Loading a file which is not a valid YAML file shall raise an UsageError.
    """
    testfile = TEST_DATA / "not_a_mapping.yml"
    with pytest.raises(exceptions.InputError):
        _ = MetaData.from_file(testfile)


def test_load_extra_parameters_are_ignored():
    """
    Any extra parameters given in the YAML file shall be silently ignored.
    """
    testfile = TEST_DATA / "metadata_with_additional_information.yml"
    metadata = MetaData.from_file(testfile)
    assert not hasattr(metadata, "additional")


def test_load_directory_passed_raises_usageerror():
    """
    If a directory name instead of a filename is given, an UsageError shall be raised.
    """
    testfile = TEST_DATA
    with pytest.raises(exceptions.InputError):
        _ = MetaData.from_file(testfile)


def test_load_file_does_not_exist_raises_input_error():
    """
    If the specified file does not exist, an InputError shall be raised.
    """
    testfile = TEST_DATA / "does_not_exist.yml"
    with pytest.raises(exceptions.InputError):
        _ = MetaData.from_file(testfile)


@pytest.mark.parametrize(
    "attribute, expected_value",
    [
        ("version", "0.0.0.0"),
        ("company_name", ""),
        ("file_description", ""),
        ("internal_name", ""),
        ("legal_copyright", ""),
        ("original_filename", ""),
        ("product_name", ""),
        ("translations", [1033, 1200]),
    ],
)
def test_from_file_missing_parameters_are_given_default_values(
    attribute, expected_value
):
    """
    It is OK to leave out any parameter in the YAML file.
    In this case, an (empty) default value will be set.
    """
    testfile = TEST_DATA / "empty_metadata.yml"
    metadata = MetaData.from_file(testfile)
    assert getattr(metadata, attribute) == expected_value


def test_load_external_version_from_file():
    """
    The 'Version' parameter can specify a filename instead of a version string.
    This filepath is seen as relative to the metadata file.
    In this case the version must be read from the file provided.
    """
    testfile = TEST_DATA / "metadata_reference_to_other_file.yml"
    metadata = MetaData.from_file(testfile)
    assert metadata.version == "4.5.6.7"


def test_validate_all_parameters_ok():
    """
    If all parameters are valid than the validation should simply return.
    """
    metadata = MetaData(**VALID_METADATA)
    metadata.validate()


@pytest.mark.parametrize(
    "attr,value",
    [
        ("version", "1.2.3.4.5"),  # "Version too long"
        ("version", "1.2.3-rc0"),  # "Wrong version syntax 1"
        ("version", "abc9.2.1"),  # "Wrong version syntax 2"
    ],
)
def test_validate_invalid_values_raise_validation_error(attr, value):
    """
    If an invalid value is given, an ValidationError must be raised.
    """
    metadata = MetaData(**VALID_METADATA)
    setattr(metadata, attr, value)

    with pytest.raises(exceptions.ValidationError):
        metadata.validate()


@pytest.mark.parametrize("attribute", VALID_METADATA.keys())
def test_sanitize_correct_values_are_not_altered(attribute):
    """
    Values which are already good to use remain untouched.
    """
    metadata = MetaData(**VALID_METADATA)
    metadata.sanitize()
    assert (
        getattr(metadata, attribute) == VALID_METADATA[attribute]
    )  # check if value is still the same as in the dictionary passed to the constructor


def test_sanitize_too_short_version_will_be_filled_with_zeros():
    """
    PyInstaller expects a version with exactly 4 places.
    If a shorter version is given, the lower parts will be filled with zeros.
    """
    metadata = MetaData(version="1.2")
    metadata.sanitize()
    assert metadata.version == "1.2.0.0"


@pytest.mark.parametrize(
    "attribute, value", [
        ("company_name", "   test   "),
        ("file_description", "   test   "),
        ("internal_name", "   test   "),
        ("legal_copyright", "   test   "),
        ("original_filename", "   test   "),
        ("product_name", "   test   "),
    ]
)
def test_sanitize_trailing_whitespace_gets_stripped(attribute, value):
    """
    Trailing whitespace in any parameter will be eliminated.
    """
    metadata = MetaData()
    setattr(metadata, attribute, value)
    metadata.sanitize()
    assert getattr(metadata, attribute) == value.strip()


def test_set_version_valid_input_overwrites_version():
    """
    It is possible to overwrite the initially set version.
    """
    metadata = MetaData(version="0.8.1.5")
    metadata.set_version("4.7.1.1")
    assert metadata.version == "4.7.1.1"


def test_set_version_invalid_input_raises_validation_error():
    """
    If something not interpretable as valid version string is passed to set_version, a ValidationError is raised.
    """
    metadata = MetaData(version="0.8.1.5")
    with pytest.raises(exceptions.ValidationError):
        metadata.set_version("this is not a valid version string")


def test_set_translations():
    """
    It is possible to set different translations / languages for the file.
    See https://learn.microsoft.com/en-us/windows/win32/menurc/varfileinfo-block#remarks
    for possible values of langID and charsetID
    """
    testfile = TEST_DATA / "metadata_with_translations.yml"
    metadata = MetaData.from_file(testfile)
    assert metadata.translations == [
        0,     # langID: language independent
        1200,  # charsetID: Unicode
        1033,  # langID: U.S. English
        1252,  # charsetID: Multilingual
    ]
