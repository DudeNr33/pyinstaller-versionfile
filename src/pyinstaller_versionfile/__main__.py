"""
Main file for pyinstaller-versionfile, which is the entrypoint for the command line script.
"""

import argparse

import pyinstaller_versionfile


def main(args=None):
    args = args or parse_args(args)
    pyinstaller_versionfile.create_versionfile_from_input_file(
        output_file=args.outfile,
        input_file=args.metadata_file,
        version=args.version
    )


def parse_args(args):
    parser = argparse.ArgumentParser(description="Create a version file for PyInstaller from a YAML metadata file.")
    parser.add_argument("metadata_file", help="Path to YAML metadata file")
    parser.add_argument("--outfile", default="./version_file.txt", help="Resulting version file for PyInstaller")
    parser.add_argument("--version", default=None, help="Override Version information given in metadata file")
    return parser.parse_args(args)


if __name__ == '__main__':  # pragma: no cover
    main()
