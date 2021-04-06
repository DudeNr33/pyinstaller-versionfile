"""
Author: Andreas Finkler

Unit tests for pyinstaller_versionfile.writer.
"""
try:
    from unittest import mock
except ImportError:
    import mock  # Python 2.7

import pytest

from pyinstaller_versionfile.writer import Writer
from pyinstaller_versionfile.exceptions import InternalUsageError, UsageError

TEST_VERSION = "0.8.1.5"
TEST_COMPANY_NAME = "TestCompany"
TEST_FILE_DESCRIPTION = "TestFileDescription"
TEST_INTERNAL_NAME = "TestInternalName"
TEST_LEGAL_COPYRIGHT = "TestLegalCopyright"
TEST_ORIGINAL_FILENAME = "TestOriginalFilename"
TEST_PRODUCT_NAME = "TestProductName"


@pytest.fixture(name="metadata_mock")
def fixture_metadata_mock():
    """
    Create a mock object for a MetaData instance that can be passed to the writer class.
    Pre-populate the 'to_dict' method to return valid content.
    The return value is taken from the 'params' attribute on the mock and can be changed easily for testing purposes.
    """
    metadata_mock = mock.MagicMock()
    metadata_mock.params = {
            "Version": TEST_VERSION,
            "CompanyName": TEST_COMPANY_NAME,
            "FileDescription": TEST_FILE_DESCRIPTION,
            "InternalName": TEST_INTERNAL_NAME,
            "LegalCopyright": TEST_LEGAL_COPYRIGHT,
            "OriginalFilename": TEST_ORIGINAL_FILENAME,
            "ProductName": TEST_PRODUCT_NAME,
        }
    metadata_mock.to_dict.return_value = metadata_mock.params
    return metadata_mock


@pytest.fixture(name="prepared_writer")
def fixture_writer(metadata_mock):
    """
    Writer object with already rendered content.
    """
    writer = Writer(metadata_mock)
    writer.render()
    return writer


@pytest.mark.parametrize(
    "attribute,value", [
        ("CompanyName", TEST_COMPANY_NAME),
        ("FileDescription", TEST_FILE_DESCRIPTION),
        ("FileVersion", TEST_VERSION),
        ("InternalName", TEST_INTERNAL_NAME),
        ("LegalCopyright", TEST_LEGAL_COPYRIGHT),
        ("OriginalFilename", TEST_ORIGINAL_FILENAME),
        ("ProductName", TEST_PRODUCT_NAME),
        ("ProductVersion", TEST_VERSION)
    ]
)
def test_render_valid_parameters_creates_correct_content(metadata_mock, attribute, value):
    """
    Check rendering of file content if provided values are complete and correct.
    """
    writer = Writer(metadata=metadata_mock)

    writer.render()

    assert "StringStruct(u'{}', u'{}')".format(attribute, value) in writer._content  # pylint: disable=protected-access


@pytest.mark.parametrize(
    "deleted_attribute",
    # pylint: disable=duplicate-code
    [
        "Version",
        "CompanyName",
        "FileDescription",
        "InternalName",
        "LegalCopyright",
        "OriginalFilename",
        "ProductName",
    ]
)
def test_render_missing_parameter_raises_internalusageerror(metadata_mock, deleted_attribute):
    """
    If any of the required parameters is missing when rendering the file content, a KeyError shall be raised.
    """
    del metadata_mock.params[deleted_attribute]
    writer = Writer(metadata=metadata_mock)

    with pytest.raises(InternalUsageError):
        writer.render()


def test_save_without_rendering_before_raises_usage_error():
    """
    Trying to write the versionfile to disk is pointless if the content has not been rendered yet.
    Since these two actions have to be triggered by the caller, he must be informed if he forgets to render before
    saving.
    """
    writer = Writer(metadata=mock.Mock())

    with pytest.raises(InternalUsageError):
        writer.save("version_file.txt")


@pytest.mark.parametrize(
    "filename",
    [
        "version_file.txt",  # most common case
        "versionfile",  # no file ending
        ".versionfile",  # leading dot
    ]
)
def test_save_valid_filepath_saves_content(prepared_writer, tmpdir, filename):
    """
    If given a valid filepath, the contents shall be saved correctly.
    """
    filepath = tmpdir / filename

    prepared_writer.save(str(filepath))

    assert filepath.read_text("utf-8") == prepared_writer._content  # pylint: disable=protected-access


def test_save_file_exists_overwrites_file(prepared_writer, tmpdir):
    """
    If the file already exists, it shall be overwritten.
    """
    filepath = tmpdir / "already_exists.txt"
    filepath.write_text("This is the previous content", "utf-8")

    prepared_writer.save(str(filepath))

    assert filepath.read_text("utf-8") == prepared_writer._content  # pylint: disable=protected-access


def test_save_directory_passed_raises_usageerror(prepared_writer, tmpdir):
    """
    If the value passed to 'save' is a directory, an IOError shall be raised.
    """
    with pytest.raises(UsageError):
        prepared_writer.save(str(tmpdir))
