"""
Unit tests for creation of the versionfile itself.
"""
from __future__ import unicode_literals

import codecs
import os

import pytest
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from pyinstaller_versionfile.create_version_file import MetaData, parse_args, main

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "../resources")
ACCEPTANCETEST_METADATA = os.path.join(RESOURCE_DIR, "acceptancetest_metadata.yml")
METADATA_EXT_VERSION_FILE = os.path.join(RESOURCE_DIR, "metadata_reference_to_other_file.yml")
METADATA_WITHOUT_VERSION = os.path.join(RESOURCE_DIR, "metadata_without_version.yml")
EXT_VERSION_FILE = os.path.join(RESOURCE_DIR, "VERSION.txt")
TEST_APP_PY_FILE = os.path.join(RESOURCE_DIR, "testapp.py")
TEST_APP_SPEC_FILE = os.path.join(RESOURCE_DIR, "testapp.spec")


@pytest.mark.parametrize(
    "version_file_attribute,metadata_key", [
        ("CompanyName", "CompanyName"),
        ("FileDescription", "FileDescription"),
        ("FileVersion", "Version"),
        ("InternalName", "InternalName"),
        ("LegalCopyright", "LegalCopyright"),
        ("OriginalFilename", "OriginalFilename"),
        ("ProductName", "ProductName"),
        ("ProductVersion", "Version")
    ]
)
def test_string_file_info(temp_version_file, version_file_attribute, metadata_key):
    MetaData(ACCEPTANCETEST_METADATA).create_version_file(outfile=temp_version_file)
    with codecs.open(temp_version_file, encoding="utf-8") as versionfile, \
            codecs.open(ACCEPTANCETEST_METADATA, encoding="utf-8") as metadata_file:
        metadata_attribute = yaml.load(metadata_file, Loader=Loader)[metadata_key]
        assert "StringStruct(u'{}', u'{}')".format(version_file_attribute, metadata_attribute) in versionfile.read()


def test_file_version_product_version_from_metadata_file(temp_version_file):
    MetaData(ACCEPTANCETEST_METADATA).create_version_file(outfile=temp_version_file)
    with codecs.open(ACCEPTANCETEST_METADATA, encoding="utf-8") as metadata_file:
        expected_version = yaml.load(metadata_file, Loader=Loader)["Version"]
    assert _version_is_set_correctly(temp_version_file, expected_version)


def test_file_version_product_version_from_explicit_version(temp_version_file):
    expected_version = "1.2.3.4"
    MetaData(ACCEPTANCETEST_METADATA, version=expected_version).create_version_file(outfile=temp_version_file)
    assert _version_is_set_correctly(temp_version_file, expected_version)


def test_file_version_product_version_from_external_file(temp_version_file):
    MetaData(METADATA_EXT_VERSION_FILE).create_version_file(outfile=temp_version_file)
    with open(EXT_VERSION_FILE) as ext_version_file:
        expected_version = ext_version_file.read().strip()
    assert _version_is_set_correctly(temp_version_file, expected_version)


@pytest.mark.parametrize(
    "given_version,expected_version",
    [
        ("1", "1.0.0.0"),
        ("1.2", "1.2.0.0"),
        ("1.2.3", "1.2.3.0"),
    ]
)
def test_fill_version_number_if_too_short(temp_version_file, given_version, expected_version):
    """
    (Issue #4)
    PyInstaller only handles version numbers with exactly 4 places.
    If a version number with less than four places is provided, pyinstaller-versionfile fills up the remaining places
    with zeros: 1.2.3 will be implicitly converted to 1.2.3.0, 1.2 will become 1.2.0.0.
    """
    MetaData(ACCEPTANCETEST_METADATA, version=given_version).create_version_file(outfile=temp_version_file)
    assert _version_is_set_correctly(temp_version_file, expected_version)


def _version_is_set_correctly(version_file, expected_version):
    with codecs.open(version_file, encoding="utf-8") as versionfile:
        content = versionfile.read()
        return (
                "filevers=({})".format(expected_version.replace(".", ",")) in content
                and "prodvers=({})".format(expected_version.replace(".", ",")) in content
                and "StringStruct(u'FileVersion', u'{}')".format(expected_version) in content
                and "StringStruct(u'ProductVersion', u'{}')".format(expected_version) in content
        )


@pytest.mark.parametrize(
    "parameter_to_check", [
        "metadata_file",
        "version",
        "outfile"
    ]
)
def test_parser(parameter_to_check):
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


@pytest.mark.parametrize(
    "parameter,expected_default_value", [
        ("outfile", "./version_file.txt"),
        ("version", None)
    ]
)
def test_default_parser_values(parameter, expected_default_value):
    parsed = parse_args(["in.yml"])
    assert getattr(parsed, parameter) == expected_default_value


def test_main(temp_version_file):
    main([METADATA_EXT_VERSION_FILE, "--outfile", temp_version_file])
    with open(EXT_VERSION_FILE) as ext_version_file:
        expected_version = ext_version_file.read().strip()
    assert _version_is_set_correctly(temp_version_file, expected_version)
