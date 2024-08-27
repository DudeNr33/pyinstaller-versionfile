"""
Main file for pyinstaller-versionfile, which is the entrypoint for the command line script.
"""

from pathlib import Path
import argparse
import sys
import json

from pyinstaller_versionfile import exceptions
import pyinstaller_versionfile


def main(args=None):
    args = args or parse_args(args)
    data = args.metadata_source

    try:
        from_json = json.loads(data)
    except Exception as err:
        if data[0] == '{' and data[-1] == '}':
            raise exceptions.InputError(f"The json similar expression {data} is invalid") from err
    else:
        data = from_json

    # from_dict
    if isinstance(data, dict):
        pyinstaller_versionfile.create_versionfile_from_dict(
            output_file=args.outfile,
            metadata=data,
            version=args.version
        )
        sys.exit(0)

    # from_yaml
    try:
        src_file = Path(data)
    except NotImplementedError as err:
        raise exceptions.InputError(f"Path {src_file.as_posix()} is invalid") from err
    else:
        if src_file.suffix == '.yaml':
            pyinstaller_versionfile.create_versionfile_from_input_file(
                output_file=args.outfile,
                input_file=src_file.as_posix(),
                version=args.version
            )
            sys.exit(0)

    # from_distribution
    pyinstaller_versionfile.create_versionfile_from_distribution(
        output_file=args.outfile,
        distname=data,
        version=args.version
    )
    sys.exit(0)


def parse_args(args):
    parser = argparse.ArgumentParser(description="Create a version file for PyInstaller from a YAML metadata file.")
    parser.add_argument("metadata_source", help="Either the path to the YAML metadata file or the name of the installed distribution.")
    parser.add_argument("--outfile", default="./version_file.txt", help="Resulting version file for PyInstaller")
    parser.add_argument("--version", default=None, help="Override Version information given in metadata file")
    return parser.parse_args(args)


if __name__ == '__main__':  # pragma: no cover
    main()
