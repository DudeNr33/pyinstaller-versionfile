"""
Author: Andreas Finkler

Functional API for programmatic use.
"""
# pylint: disable=too-many-arguments, too-many-positional-arguments

from typing import Optional

from pyinstaller_versionfile.metadata import MetaData
from pyinstaller_versionfile.writer import Writer


def create_versionfile(
    output_file: str,
    version: Optional[str] = None,
    company_name: Optional[str] = None,
    file_description: Optional[str] = None,
    internal_name: Optional[str] = None,
    legal_copyright: Optional[str] = None,
    original_filename: Optional[str] = None,
    product_name: Optional[str] = None,
    translations: Optional[list[int]] = None,
) -> None:
    """
    Create a new versionfile from the information given.
    All parameters except output_file are optional and will be replaced with placeholder values
    if not specified.
    """
    metadata = MetaData(
        version=version,
        company_name=company_name,
        file_description=file_description,
        internal_name=internal_name,
        legal_copyright=legal_copyright,
        original_filename=original_filename,
        product_name=product_name,
        translations=translations,
    )
    __create(metadata, output_file)


def create_versionfile_from_input_file(
    output_file: str,
    input_file: str,
    version: Optional[str] = None,
    company_name: Optional[str] = None,
    file_description: Optional[str] = None,
    internal_name: Optional[str] = None,
    legal_copyright: Optional[str] = None,
    original_filename: Optional[str] = None,
    product_name: Optional[str] = None,
    translations: Optional[list[int]] = None,
) -> None:
    """
    Create a new versionfile from metadata specified in input_file.
    If the version argument is set, the version specified in input_file will be overwritten with the value
    of version.
    """
    metadata = MetaData.from_file(
        input_file,
        version=version,
        company_name=company_name,
        file_description=file_description,
        internal_name=internal_name,
        legal_copyright=legal_copyright,
        original_filename=original_filename,
        product_name=product_name,
        translations=translations,
    )
    if version:
        metadata.set_version(version)
    __create(metadata, output_file)


def create_versionfile_from_distribution(
    output_file: str,
    distname: str,
    version: Optional[str] = None,
    company_name: Optional[str] = None,
    file_description: Optional[str] = None,
    internal_name: Optional[str] = None,
    legal_copyright: Optional[str] = None,
    original_filename: Optional[str] = None,
    product_name: Optional[str] = None,
    translations: Optional[list[int]] = None,
) -> None:
    """
    Create a new versionfile from metadata that are stored in distribution
    addressed by `distname`. If the `version` argument is set, the version specified
    in distribution will be overwritten.

    This function can be helpful with regard to the automatic versioning of
    packages.
    """
    metadata = MetaData.from_distribution(
        distname,
        version=version,
        company_name=company_name,
        file_description=file_description,
        internal_name=internal_name,
        legal_copyright=legal_copyright,
        original_filename=original_filename,
        product_name=product_name,
        translations=translations,
    )
    if version:
        metadata.set_version(version)
    __create(metadata, output_file)


def __create(metadata: MetaData, output_file: str) -> None:
    metadata.validate()
    metadata.sanitize()
    writer = Writer(metadata)
    writer.render()
    writer.save(output_file)
