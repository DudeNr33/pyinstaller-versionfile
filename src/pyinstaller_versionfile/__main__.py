"""
Main file for pyinstaller-versionfile, which is the entrypoint for the command line script.
"""

from typing import Sequence, Optional, Union

import argparse
from argparse import Namespace

import pyinstaller_versionfile
from pyinstaller_versionfile import exceptions


def make_version(args: Union[Namespace, Optional[Sequence[str]]] = None) -> None:
    if not isinstance(args, Namespace):
        args = parse_args_make_version(args)

    optional_args = {
        "version": args.version,
        "company_name": args.company_name,
        "file_description": args.file_description,
        "internal_name": args.internal_name,
        "legal_copyright": args.legal_copyright,
        "original_filename": args.original_filename,
        "product_name": args.product_name,
    }

    if args.source_format == "yaml":
        pyinstaller_versionfile.create_versionfile_from_input_file(
            output_file=args.outfile,
            input_file=args.metadata_source,
            **optional_args,
        )
    elif args.source_format in ["distribution", "dist"]:
        pyinstaller_versionfile.create_versionfile_from_distribution(
            output_file=args.outfile,
            distname=args.metadata_source,
            **optional_args,
        )
    else:
        pyinstaller_versionfile.create_versionfile(
            output_file=args.outfile,
            **optional_args,
        )


def parse_args_make_version(args: Optional[Sequence[str]]) -> Namespace:
    parser = argparse.ArgumentParser(
        description="Create a version file for PyInstaller."
    )
    parser.add_argument(
        "--metadata-source",
        help="Required if --source-format is specified. Either path to the input file, or name of the distribution.",
    )
    parser.add_argument(
        "--source-format",
        choices=["yaml", "distribution", "dist"],
        help="Define the source format expected in --metadata-source.",
    )
    parser.add_argument(
        "--outfile",
        default="./version_file.txt",
        help="Resulting version file for PyInstaller.",
    )
    parser.add_argument(
        "--version",
        default=None,
        help="Override Version information given in metadata file.",
    )
    parser.add_argument(
        "--company-name",
        default=None,
        help="Name of the company that produced the file.",
    )
    parser.add_argument(
        "--file-description",
        default=None,
        help=(
            "Description to be presented to users. "
            "It may be displayed when the user is choosing files to install."
        ),
    )
    parser.add_argument(
        "--internal-name",
        default=None,
        help=(
            "Internal name of the file. "
            "If the file has no internal name, this string should be the original filename, without extension."
        ),
    )
    parser.add_argument(
        "--legal-copyright",
        default=None,
        help=(
            "Copyright notices that apply to the file. "
            "This should include the full text of all notices, legal symbols, copyright dates, and so on."
        ),
    )
    parser.add_argument(
        "--original-filename",
        default=None,
        help=(
            "Original name of the file, not including a path. "
            "This information enables an application to determine whether a file has been renamed by a user."
        ),
    )
    parser.add_argument(
        "--product-name",
        default=None,
        help="Name of the product with which the file is distributed.",
    )

    # TODO: idea for translation? Maybe langID=0;charsetID=1200? or just <langID>:<charsetID>?  pylint: disable=fixme
    parsed_args = parser.parse_args(args)
    if parsed_args.source_format and not parsed_args.metadata_source:
        parser.error("--metadata-source is required if --source-format is specified.")
    return parsed_args


def create_version_file(args: Union[Namespace, Optional[Sequence[str]]] = None) -> None:
    if not isinstance(args, Namespace):
        args = parse_args_create_version_file(args)
    if args.source_format == "yaml":
        # from_yaml
        pyinstaller_versionfile.create_versionfile_from_input_file(
            output_file=args.outfile,
            input_file=args.metadata_source,
            version=args.version,
        )
    elif args.source_format in ["distribution", "dist"]:
        # from_distribution
        pyinstaller_versionfile.create_versionfile_from_distribution(
            output_file=args.outfile,
            distname=args.metadata_source,
            version=args.version,
        )
    else:
        # because of 'choises' in --source-format this case should not be entered
        raise exceptions.InternalUsageError(
            "Unexpected behaviour in main. Please check parser definition."
        )


def parse_args_create_version_file(args: Optional[Sequence[str]]) -> Namespace:
    parser = argparse.ArgumentParser(
        description="Create a version file for PyInstaller from a YAML metadata file."
    )
    parser.add_argument(
        "metadata_source",
        help="Either the path to the YAML metadata file or the name of the installed distribution.",
    )
    parser.add_argument(
        "--source-format",
        choices=["yaml", "distribution", "dist"],
        default="yaml",
        help="Define the source format expected in metadata_source",
    )
    parser.add_argument(
        "--outfile",
        default="./version_file.txt",
        help="Resulting version file for PyInstaller",
    )
    parser.add_argument(
        "--version",
        default=None,
        help="Override Version information given in metadata file",
    )
    return parser.parse_args(args)


if __name__ == "__main__":  # pragma: no cover
    create_version_file()
