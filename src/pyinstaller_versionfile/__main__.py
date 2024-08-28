"""
Main file for pyinstaller-versionfile, which is the entrypoint for the command line script.
"""
import argparse
import sys

from pyinstaller_versionfile import exceptions
import pyinstaller_versionfile


def main(args=None):
    args = args or parse_args(args)
    if args.source_format == "yaml":
        # from_yaml
        pyinstaller_versionfile.create_versionfile_from_input_file(
            output_file=args.outfile,
            input_file=args.metadata_source,
            version=args.version
        )
    elif args.source_format in ['distribution', 'dist']:
        # from_distribution
        pyinstaller_versionfile.create_versionfile_from_distribution(
            output_file=args.outfile,
            distname=args.metadata_source,
            version=args.version
        )
    else:
        # because of 'choises' in --source-format this case should not be entered 
        raise exceptions.InternalUsageError(f"Unexpected behaviour in main. Please check parser definition.")

    sys.exit(0)


def parse_args(args):
    parser = argparse.ArgumentParser(description="Create a version file for PyInstaller from a YAML metadata file.")
    parser.add_argument(
        "metadata_source",
        help="Either the path to the YAML metadata file or the name of the installed distribution."
    )
    parser.add_argument(
        "--source-format",
        choices=["yaml", "distribution", "dist"],
        default="yaml", help="Define the source format expected in metadata_source"
    )
    parser.add_argument("--outfile", default="./version_file.txt", help="Resulting version file for PyInstaller")
    parser.add_argument("--version", default=None, help="Override Version information given in metadata file")
    return parser.parse_args(args)


if __name__ == '__main__':  # pragma: no cover
    main()
