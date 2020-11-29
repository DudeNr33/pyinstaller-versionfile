"""
Author: Andreas Finkler
"""
import codecs
# noinspection PyCompatibility
from pathlib import Path

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:  # pragma: no cover
    from yaml import Loader


class MetaData(object):
    """
    Read and validate the metadata provided for versionfile generation.
    """
    def __init__(self):
        self.version = None
        self.company_name = None
        self.file_description = None
        self.internal_name = None
        self.legal_copyright = None
        self.original_filename = None
        self.product_name = None

    def load(self, filepath):
        """
        Load the metadata from the given file.
        """
        with codecs.open(filepath, encoding="utf-8") as infile:
            data = yaml.load(infile, Loader=Loader)
        version = data.get("Version", "")
        path = (Path(filepath).parent/version)
        if path.is_file():
            self.version = path.read_text().strip()
        else:
            self.version = version
        self.company_name = data.get("CompanyName", "")
        self.file_description = data.get("FileDescription", "")
        self.internal_name = data.get("InternalName", "")
        self.legal_copyright = data.get("LegalCopyright", "")
        self.original_filename = data.get("OriginalFilename", "")
        self.product_name = data.get("ProductName", "")

    def set_version(self, version_string):
        """
        Explicitly set the version. Overwrites the existing version if already set.
        """
        self.version = version_string

    def validate(self):
        """
        Check if the supplied parameters are correct and understandable by PyInstaller.
        """

    def sanitize(self):
        """
        Convert valid but insufficient input (e.g. too short version number) and perform some aesthetic work like
        stripping trailing whitespace.
        """

    def to_dict(self):
        """
        Return all values necessary for rendering the template as dictionary.
        """
        return {
            "Version": self.version,
            "CompanyName": self.company_name,
            "FileDescription": self.file_description,
            "InternalName": self.internal_name,
            "LegalCopyright": self.legal_copyright,
            "OriginalFilename": self.original_filename,
            "ProductName": self.product_name,
        }
