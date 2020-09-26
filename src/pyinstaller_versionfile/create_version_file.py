import argparse
import codecs
import os.path

import yaml
from jinja2 import Template

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

TEMPLATE_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "version_file_template.txt")


class MetaData(object):
    def __init__(self, metadata_file, version=None):
        self._filepath = metadata_file
        self._metadata = None
        self._version = version

    def create_version_file(self, outfile):
        self._read_metadata_from_file()
        if self._explicit_version_was_provided():
            self._override_version()
        elif self._refers_to_external_version_file():
            self._read_version_from_external_file()
        self._render_version_file(outfile)

    def _read_metadata_from_file(self):
        with codecs.open(self._filepath, encoding="utf-8") as infile:
            self._metadata = yaml.load(infile, Loader=Loader)

    def _explicit_version_was_provided(self):
        return self._version is not None

    def _override_version(self):
        self._metadata["Version"] = self._version

    def _refers_to_external_version_file(self):
        return os.path.isfile(os.path.join(os.path.dirname(self._filepath), self._metadata["Version"]))

    def _read_version_from_external_file(self):
        with open(os.path.join(os.path.dirname(self._filepath), self._metadata["Version"])) as infile:
            self._metadata["Version"] = infile.read().strip()

    def _render_version_file(self, outfile):
        with codecs.open(TEMPLATE_FILE, encoding="utf-8") as infile:
            template = Template(infile.read())
        with codecs.open(outfile, "w", encoding="utf-8") as outfile:
            outfile.write(template.render(**self._metadata))


def main(args=None):
    args = parse_args(args)
    MetaData(args.metadata_file, args.version).create_version_file(args.outfile)


def parse_args(args):
    parser = argparse.ArgumentParser(description="Create a version file for PyInstaller from a YAML metadata file.")
    parser.add_argument("metadata_file", help="Path to YAML metadata file")
    parser.add_argument("--outfile", default="./version_file.txt", help="Resulting version file for PyInstaller")
    parser.add_argument("--version", default=None, help="Override Version information given in metadata file")
    return parser.parse_args(args)


if __name__ == '__main__':
    main()
