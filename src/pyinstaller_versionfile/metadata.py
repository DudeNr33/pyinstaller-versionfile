"""
Author: Andreas Finkler
"""
# pylint: disable=too-many-arguments, too-many-positional-arguments
from __future__ import annotations
from typing import Optional, Union, TypedDict, Any

import codecs
import re
import itertools
from pathlib import Path

from importlib.metadata import PackageNotFoundError, distribution

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:  # pragma: no cover
    from yaml import Loader  # type: ignore

from pyinstaller_versionfile import exceptions


class MetadataKwargs(TypedDict, total=False):
    """Helper class to specify type hints for the kwargs used in some of the methods."""
    version: Optional[str]
    company_name: Optional[str]
    file_description: Optional[str]
    internal_name: Optional[str]
    legal_copyright: Optional[str]
    original_filename: Optional[str]
    product_name: Optional[str]
    translations: Optional[list[int]]


class MetaData:
    """
    Read and validate the metadata provided for versionfile generation.
    """

    placeholder_value = ""  # value to use if nothing was specified
    default_translations = [1033, 1200]
    key_conversion = {
        "Version": "version",
        "CompanyName": "company_name",
        "FileDescription": "file_description",
        "InternalName": "internal_name",
        "LegalCopyright": "legal_copyright",
        "OriginalFilename": "original_filename",
        "ProductName": "product_name",
        "Translation": "translations",
    }

    def __init__(
        self,
        version: Optional[str]=None,
        company_name: Optional[str]=None,
        file_description: Optional[str]=None,
        internal_name: Optional[str]=None,
        legal_copyright: Optional[str]=None,
        original_filename: Optional[str]=None,
        product_name: Optional[str]=None,
        translations: Optional[list[int]]=None,
    ) -> None:
        self.version = version or "0.0.0.0"
        self.company_name = company_name or self.placeholder_value
        self.file_description = file_description or self.placeholder_value
        self.internal_name = internal_name or self.placeholder_value
        self.legal_copyright = legal_copyright or self.placeholder_value
        self.original_filename = original_filename or self.placeholder_value
        self.product_name = product_name or self.placeholder_value
        self.translations = translations or self.default_translations

    @classmethod
    # better type hint for typing.Unpack[MetadataKwargs] requires at least Python 3.11
    def from_distribution(cls, distname: str, **kwargs: Any) -> MetaData:
        """
        Factory method to extract metadata from installed packages.
        """
        try:
            dist = distribution(distname)
            meta = dist.metadata
        except PackageNotFoundError as err:  # pragma: no cover
            raise exceptions.InputError(f"Distribution {distname} not found") from err

        meta_fields = [
            meta.get("Author", None),
            meta.get("Author-email", None),
            meta.get("Maintainer", None),
            meta.get("Maintainer-email", None),
            meta.get("Home-page", None),
        ]
        company = ", ".join([field for field in meta_fields if field])

        kwargs.setdefault("version", meta.get("Version", None))
        kwargs.setdefault("company_name", company)
        kwargs.setdefault("file_description", meta.get("Summary", None))
        kwargs.setdefault("internal_name", meta.get("Name", None))
        kwargs.setdefault("legal_copyright", meta.get("License", None))
        kwargs.setdefault("original_filename", meta.get("Name", None))
        kwargs.setdefault("product_name", meta.get("Name", None))
        kwargs.setdefault(
            "translations", cls.default_translations
        )

        return cls(**kwargs)

    @classmethod
    def from_file(cls, filepath: str, **kwargs: Any) -> MetaData:
        """
        Factory method to create a MetaData instance from a file.
        """
        try:
            with codecs.open(filepath, encoding="utf-8") as infile:
                data = yaml.load(infile, Loader=Loader)
        except IsADirectoryError as err:
            raise exceptions.InputError(
                f"Specified filepath {filepath} is a directory, not a file"
            ) from err
        except FileNotFoundError as err:
            raise exceptions.InputError(f"File {filepath} does not exist") from err
        except IOError as err:
            raise exceptions.InputError("Failed to read input from file") from err
        except yaml.scanner.ScannerError as err:
            raise exceptions.InputError(
                "Failed to read YAML data due to scanner error"
            ) from err
        if not isinstance(data, dict):
            raise exceptions.InputError(
                f"Input file must contain a mapping, but is: {type(data)}"
            )

        data = {
            cls.key_conversion[k]: v for k, v in data.items() if k in cls.key_conversion
        }
        data.update({k: v for k, v in kwargs.items() if v is not None})

        version = data.get("version", "0.0.0.0")
        path = Path(filepath).parent / version
        if path.is_file():
            version = path.read_text().strip()
            data["version"] = version
        data["translations"] = cls._get_translations(data.get("translations"))

        return cls(**data)

    @classmethod
    def _get_translations(cls, data: Optional[list[dict[str, int]]]) -> list[int]:
        if not data:
            return cls.default_translations
        # The version file requires a flat list, where the first two values form the first
        # pair of language and charset, the third and fourth form the second pair, and so on.
        # For better readability the metadata file uses a list of dictionaries here, so we have
        # to flatten it first
        return list(
            itertools.chain(*[(d["langID"], d["charsetID"]) for d in data])
        )

    def set_version(self, version_string: str) -> None:
        """
        Explicitly set the version. Overwrites the existing version if already set.
        """
        self.__validate_version(version_string)
        self.version = version_string

    def validate(self) -> None:
        """
        Check if the supplied parameters are correct and understandable by PyInstaller.
        """
        self.__validate_version(self.version)

    @staticmethod
    def __validate_version(version: str) -> None:
        version_regex = r"\d+(\.\d+){0,3}"
        if not re.fullmatch(pattern=version_regex, string=version):
            raise exceptions.ValidationError(
                f"Provided version {version} is not valid. "
                "Valid versions must contain four places with only digits."
            )

    def sanitize(self) -> None:
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

    def to_dict(self) -> dict[str, Union[str, list[int]]]:
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
