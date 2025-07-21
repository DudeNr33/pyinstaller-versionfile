import os
import typing as t
from pathlib import Path

import PyInstaller.utils.win32.versioninfo as vi
import pytest

import pyinstaller_versionfile
from pyinstaller_versionfile.metadata import MetadataKwargs


def read_versionfile(
    versionfile: t.Union[str, os.PathLike],
    lazy: bool = True,
) -> MetadataKwargs:
    """
    Parse a PyInstaller version info text file and extract metadata.

    Args:
        file: Path to the version info text file
        lazy: If True, unknown or missing fields will be skipped without raising an error.

    Returns:
        MetadataKwargs: Dictionary with extracted metadata
    """
    versioninfo = vi.load_version_info_from_text_file(
        str(versionfile)
    )  # type: vi.VSVersionInfo

    kwargs = {}

    for info in versioninfo.kids:
        if type(info) is vi.StringFileInfo:
            for kid in filter(lambda x: x.name == "040904B0", info.kids):
                for item in kid.kids:
                    try:
                        kwargs[item.name] = item.val
                    except Exception as e:
                        raise RuntimeError(f"Error processing '{item!r}'") from e
                else:
                    break
            else:
                if lazy is False:
                    raise ValueError(
                        f"Expected '040904B0' StringTable in StringFileInfo, but not found: {info!r}"
                    )
        elif type(info) is vi.VarFileInfo:
            for kid in filter(lambda x: x.name == "Translation", info.kids):
                try:
                    kwargs[kid.name] = kid.kids
                except Exception as e:
                    raise RuntimeError(f"Error processing '{repr(kid)}'") from e
                else:
                    break
            else:
                if lazy is False:
                    raise ValueError(
                        f"Expected 'Translation' VarStruct in VarFileInfo, but not found: {info!r}"
                    )
        else:
            if lazy is False:
                raise ValueError(f"Unexpected type in version info: '{info!r}'")

    return MetadataKwargs(
        version=kwargs.get("FileVersion"),
        company_name=kwargs.get("CompanyName"),
        file_description=kwargs.get("FileDescription"),
        internal_name=kwargs.get("InternalName"),
        legal_copyright=kwargs.get("LegalCopyright"),
        original_filename=kwargs.get("OriginalFilename"),
        product_name=kwargs.get("ProductName"),
        # product_version = kwargs.get("ProductVersion"), # not used in MetadataKwargs
        translations=kwargs.get("Translation"),
    )


@pytest.mark.parametrize(
    "distname",
    [
        "pip",
        "pyinstaller_versionfile",
    ],
)
def test_distribution(distname: str, tmp_path: Path) -> None:
    """test failes if any value of the versionfile is an empty string."""

    output_file = tmp_path / "version_file.txt"

    assert output_file.is_file() is False, f"{output_file=!s} already exists."

    pyinstaller_versionfile.create_versionfile_from_distribution(
        output_file=str(output_file),
        distname=distname,
    )

    assert output_file.is_file(), f"{output_file=!s} was not created."

    metadata = read_versionfile(output_file, lazy=False)

    assert not any(
        v == "" for v in metadata.values()
    ), "Metadata fields should not be empty."


@pytest.mark.parametrize(
    "distname",
    [
        "pip",
        "pyinstaller_versionfile",
    ],
)
@pytest.mark.parametrize(
    "params",
    [
        {"version": "9.8.7.6"},
        {"company_name": "fubar inc."},
        {"translations": [1234, 4321]},
    ],
    ids=repr,
)
def test_distribution_params(
    distname: str,
    tmp_path: Path,
    params: dict[str, t.Any],
) -> None:
    """test failes if given parameters are not set in the versionfile."""

    output_file: Path = tmp_path / "version_file.txt"

    assert output_file.is_file() is False, f"{output_file=!s} already exists."

    pyinstaller_versionfile.create_versionfile_from_distribution(
        output_file=str(output_file),
        distname=distname,
        **params,
    )

    assert output_file.is_file(), f"{output_file=!s} was not created."

    metadata = read_versionfile(output_file, lazy=False)

    for key, val in params.items():
        value = metadata.get(key)
        assert (
            value == val
        ), f"Expected getattr(metadata, {key!r})=={val!r}, but got {value!r}"
