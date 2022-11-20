"""
Author: Andreas Finkler
"""
import codecs
import re
import itertools
# noinspection PyCompatibility
from pathlib import Path

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:  # pragma: no cover
    from yaml import Loader

from pyinstaller_versionfile import exceptions


class MetaData(object):
    """
    Read and validate the metadata provided for versionfile generation.
    """
    placeholder_value = ""  # value to use if nothing was specified
    default_translations = [1033, 1200]

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        version=None,
        company_name=None,
        file_description=None,
        internal_name=None,
        legal_copyright=None,
        original_filename=None,
        product_name=None,
        translations=None
    ):
        self.version = version or "0.0.0.0"
        self.company_name = company_name or self.placeholder_value
        self.file_description = file_description or self.placeholder_value
        self.internal_name = internal_name or self.placeholder_value
        self.legal_copyright = legal_copyright or self.placeholder_value
        self.original_filename = original_filename or self.placeholder_value
        self.product_name = product_name or self.placeholder_value
        self.translations = translations or self.default_translations

    @classmethod
    def from_file(cls, filepath):
        """
        Factory method to create a MetaData instance from a file.
        """
        try:
            with codecs.open(filepath, encoding="utf-8") as infile:
                data = yaml.load(infile, Loader=Loader)
        except IsADirectoryError as err:
            raise exceptions.InputError(f"Specified filepath {filepath} is a directory, not a file") from err
        except FileNotFoundError as err:
            raise exceptions.InputError(f"File {filepath} does not exist") from err
        except IOError as err:
            raise exceptions.InputError("Failed to read input from file") from err
        except yaml.scanner.ScannerError as err:
            raise exceptions.InputError("Failed to read YAML data due to scanner error") from err
        if not isinstance(data, dict):
            raise exceptions.InputError(f"Input file must contain a mapping, but is: {type(data)}")
        version = data.get("Version", "0.0.0.0")
        path = (Path(filepath).parent/version)
        if path.is_file():
            version = path.read_text().strip()
        translations = cls._get_translations(data)
        return cls(
            version=version,
            company_name=data.get("CompanyName"),
            file_description=data.get("FileDescription"),
            internal_name=data.get("InternalName"),
            legal_copyright=data.get("LegalCopyright"),
            original_filename=data.get("OriginalFilename"),
            product_name=data.get("ProductName"),
            translations=translations,
        )

    @classmethod
    def _get_translations(cls, data):
        input_data = data.get("Translation")
        if not input_data:
            return cls.default_translations
        # The version file requires a flat list, where the first two values form the first
        # pair of language and charset, the third and fourth form the second pair, and so on.
        # For better readability the metadata file uses a list of dictionaries here, so we have
        # to flatten it first
        return list(itertools.chain(*[(d["langID"], d["charsetID"]) for d in input_data]))

    def set_version(self, version_string):
        """
        Explicitly set the version. Overwrites the existing version if already set.
        """
        self.__validate_version(version_string)
        self.version = version_string

    def validate(self):
        """
        Check if the supplied parameters are correct and understandable by PyInstaller.
        """
        self.__validate_version(self.version)

    @staticmethod
    def __validate_version(version):
        version_regex = r"\d+(\.\d+){0,3}"
        if not re.fullmatch(pattern=version_regex, string=version):
            raise exceptions.ValidationError(
                f"Provided version {version} is not valid. " \
                "Valid versions must contain four places with only digits."
            )

    def sanitize(self):
        """
        Convert valid but insufficient input (e.g. too short version number) and perform some aesthetic work like
        stripping trailing whitespace.
        """
        required_length = 4
        version_length = len(self.version.split("."))
        if version_length < required_length:
            missing_places = required_length - version_length
            self.version += ".0" * missing_places
        for key, value in self.__dict__.items():
            if isinstance(value, str):
                setattr(self, key, value.strip())

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
            "Translation": self.translations,
        }
