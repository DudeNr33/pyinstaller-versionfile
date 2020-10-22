# pyinstaller-versionfile
![GitHub](https://img.shields.io/github/license/dudenr33/pyinstaller-versionfile) 
![PyPI](https://img.shields.io/pypi/v/pyinstaller-versionfile)
![Travis (.com) branch](https://img.shields.io/travis/com/dudenr33/pyinstaller-versionfile/master)
![Codecov](https://img.shields.io/codecov/c/github/dudenr33/pyinstaller-versionfile/master)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyinstaller-versionfile)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/DudeNr33/pyinstaller-versionfile)

Create a windows version-file from a simple YAML file that can be used by PyInstaller.

## Background
Pyinstaller provides a way to [capture Windows version data](https://pyinstaller.readthedocs.io/en/stable/usage.html#capturing-windows-version-data)
through a so called _version-file_. The process of crafting such a version file, and especially keeping the version number
updated, is a bit cumbersome. 
This package aims to make the creation of such a version file easier.

## Usage
pyinstaller-versionfile provides a command line interface to convert a simple YAML file into a version-file suitable
to pass to PyInstaller via the `--version-file=` option.

A complete YAML configuration looks like this:
```YAML
Version: 1.2.3.4
CompanyName: My Imaginary Company
FileDescription: Simple App
InternalName: Simple App
LegalCopyright: © My Imaginary Company. All rights reserved.
OriginalFilename: SimpleApp.exe
ProductName: Simple App
```
The encoding must be UTF-8.

To create version-file from this, simple run:
```cmd
create-version-file metadata.yml --outfile file_version_info.txt
```
where metadata.yml is the YAML configuration file from above.


### Extracting Version Information
As an alternative to specifying the version directly in the YAML file, there are two alternatives which may be more
suitable, depending on the use case:

#### Link to an External File
Instead of writing the version string directly into the YAML file, you can also specify the (relative) path to another
file. Note that this file must only contain the version string and nothing else.

```YAML
Version: VERSION.txt
CompanyName: My Imaginary Company
FileDescription: Simple App
InternalName: Simple App
LegalCopyright: © My Imaginary Company. All rights reserved.
OriginalFilename: SimpleApp.exe
ProductName: Simple App
```

#### Setting the Version from the Command Line
It is also possible to set the version directly over the command line using the `--version` option:
```cmd
create-version-file metadata.yml --outfile file_version_info.txt --version 0.8.1.5
```
This can be useful if you want to use a CI build number as the version. 
