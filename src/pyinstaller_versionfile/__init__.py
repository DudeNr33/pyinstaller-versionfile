"""
Author: Andreas Finkler

Functional API for programmatic use.
"""
from pyinstaller_versionfile.metadata import MetaData
from pyinstaller_versionfile.writer import Writer


def create_versionfile(
    output_file,
    version=None,
    company_name=None,
    file_description=None,
    internal_name=None,
    legal_copyright=None,
    original_filename=None,
    product_name=None,
    translations=None,
):  # pylint: disable=too-many-arguments
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


def create_versionfile_from_input_file(output_file, input_file, version=None):
    """
    Create a new versionfile from metadata specified in input_file.
    If the version argument is set, the version specified in input_file will be overwritten with the value
    of version.
    """
    metadata = MetaData.from_file(input_file)
    if version:
        metadata.set_version(version)
    __create(metadata, output_file)


def __create(metadata, output_file):
    metadata.validate()
    metadata.sanitize()
    writer = Writer(metadata)
    writer.render()
    writer.save(output_file)
