from __future__ import unicode_literals

import codecs
import os
import subprocess
import sys
import tempfile

import pytest
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from pyinstaller_versionfile.create_version_file import MetaData, parse_args

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "resources")
ACCEPTANCETEST_METADATA = os.path.join(RESOURCE_DIR, "acceptancetest_metadata.yml")
METADATA_EXT_VERSION_FILE = os.path.join(RESOURCE_DIR, "metadata_reference_to_other_file.yml")
EXT_VERSION_FILE = os.path.join(RESOURCE_DIR, "VERSION.txt")
TEST_APP_PY_FILE = os.path.join(RESOURCE_DIR, "testapp.py")
TEST_APP_SPEC_FILE = os.path.join(RESOURCE_DIR, "testapp.spec")


def get_version_number(filename):
    from win32api import GetFileVersionInfo, LOWORD, HIWORD
    try:
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return "{}.{}.{}.{}".format(HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls))
    except:  # noqa
        return None


@pytest.fixture()
def temp_dir():
    tempdirobj = None
    try:
        tempdirobj = tempfile.TemporaryDirectory(dir=tempfile.gettempdir())
        dirname = tempdirobj.name
    except AttributeError:
        # Python 2.7 does not have tempfile.TemporaryDirectory
        dirname = tempfile.mkdtemp()
    yield dirname
    if tempdirobj:
        tempdirobj.cleanup()
    else:
        import shutil
        shutil.rmtree(dirname)


@pytest.fixture()
def temp_version_file(temp_dir):
    return os.path.join(temp_dir, "version_file.txt")


@pytest.mark.skipif(
    not sys.platform.startswith("win") or os.environ.get("includeE2E", "False") != "True",
    reason="Long running test, only possible on windows OS.")
def test_end2end_exe_generation(temp_dir, temp_version_file):
    """
    Checks if pyinstaller is able to interpret the generated version file and if the generated EXE has the correct
    version info.
    Other attributes are not checked for.
    """
    with open(ACCEPTANCETEST_METADATA) as infile:
        metadata = yaml.load(infile, Loader=Loader)
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


@pytest.mark.skipif(os.environ.get("includeE2E", "False") != "True", reason="Only possbile in tox environment.")
def test_end2end_version_file_creation(temp_version_file):
    returncode = subprocess.call(
        [
            "create-version-file",
            ACCEPTANCETEST_METADATA,
            "--outfile", temp_version_file,
            "--version", "0.8.1.5"
        ]
    )
    assert returncode == 0
    assert os.path.isfile(temp_version_file)


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
