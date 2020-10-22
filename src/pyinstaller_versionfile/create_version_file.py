"""
Author: Andreas Finkler

Main module for pyinstaller-versionfile.
"""
import argparse
import codecs
import os.path

import yaml
from packaging import version as pkgversion
from jinja2 import Template

try:
    from yaml import CLoader as Loader
except ImportError:  # pragma: no cover
    from yaml import Loader

TEMPLATE_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "version_file_template.txt")


# pylint: disable=too-few-public-methods
class MetaData(object):
    """
    This class handles the conversion from a metadata YAML file to a versionfile understandable by PyInstaller.
    """
    def __init__(self, metadata_file, version=None):
        self._filepath = metadata_file
        self._metadata = None
        self._explicitly_defined_version = version

    def create_version_file(self, outfile):
        self._read_metadata_from_file()
        if self._explicit_version_was_provided():
            self._override_version()
        elif self._refers_to_external_version_file():
            self._read_version_from_external_file()
        if self._version_is_too_short():
            self._fill_version()
        self._render_version_file(outfile)

    def _read_metadata_from_file(self):
        with codecs.open(self._filepath, encoding="utf-8") as infile:
            self._metadata = yaml.load(infile, Loader=Loader)

    def _explicit_version_was_provided(self):
        return self._explicitly_defined_version is not None

    def _override_version(self):
        self._metadata["Version"] = self._explicitly_defined_version

    def _refers_to_external_version_file(self):
        if "Version" not in self._metadata:
            return False
        return os.path.isfile(os.path.join(os.path.dirname(self._filepath), self._metadata["Version"]))

    def _read_version_from_external_file(self):
        with open(os.path.join(os.path.dirname(self._filepath), self._metadata["Version"])) as infile:
            self._metadata["Version"] = infile.read().strip()

    def _version_is_too_short(self):
        specified_version = pkgversion.parse(self._metadata["Version"])
        return len(specified_version.release) < 4

    def _fill_version(self):
        new_version = [0, 0, 0, 0]
        specified_version = pkgversion.parse(self._metadata["Version"])
        for index, version_part in enumerate(specified_version.release):
            new_version[index] = version_part
        self._metadata["Version"] = ".".join(str(part) for part in new_version)

    def _render_version_file(self, outfile):
        with codecs.open(TEMPLATE_FILE, encoding="utf-8") as infile:
            template = Template(infile.read())
        with codecs.open(outfile, "w", encoding="utf-8") as file_handle:
            file_handle.write(template.render(**self._metadata))


def main(args=None):
    args = parse_args(args)
    MetaData(args.metadata_file, args.version).create_version_file(args.outfile)


def parse_args(args):
    parser = argparse.ArgumentParser(description="Create a version file for PyInstaller from a YAML metadata file.")
    parser.add_argument("metadata_file", help="Path to YAML metadata file")
    parser.add_argument("--outfile", default="./version_file.txt", help="Resulting version file for PyInstaller")
    parser.add_argument("--version", default=None, help="Override Version information given in metadata file")
    return parser.parse_args(args)


if __name__ == '__main__':  # pragma: no cover
    main()
