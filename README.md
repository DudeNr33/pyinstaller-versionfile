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

The key/value pairs that be specified in the version file and [their official meaning](https://docs.microsoft.com/en-us/windows/win32/menurc/stringfileinfo-block) are shown the following table:

| Parameter Name | Description |
|:---:|---|
| CompanyName | Name of the company that produced the file, for example, "My Imaginary Company, Inc.". |
| FileDescription | Description to be presented to users. It may be displayed when the user is choosing files to install. For example, "A simple app that does simple things.". |
| InternalName | Internal name of the file. If the file has no internal name, this string should be the original filename, without extension. For example, 'Simple App". |
| LegalCopyright | Copyright notices that apply to the file. This should include the full text of all notices, legal symbols, copyright dates, and so on. For example, "Copyright © 2000-2022, My Imaginary Company, Inc. All rights reserved.". |
| OriginalFilename | Original name of the file, not including a path. This information enables an application to determine whether a file has been renamed by a user. For example, "SimpleApp.exe". |
| ProductName | Name of the product with which the file is distributed, for example, "Simple App". |
| Translation | Combinations of language and character sets supported by the application. See [the documentation](https://learn.microsoft.com/en-us/windows/win32/menurc/varfileinfo-block#remarks) for the codes to use. Multiple values can be specified. |

## Usage
pyinstaller-versionfile provides both a command line interface and a functional API.

### Command line interface
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
Translation:
  - langID: 0
    charsetID: 1200
  - langID: 1033
    charsetID: 1252
```
The encoding must be UTF-8. All fields are optional, you can choose to specify only those that are of interest to you.

To create version-file from this, simple run:
```cmd
create-version-file metadata.yml --outfile file_version_info.txt
```
where metadata.yml is the YAML configuration file from above.


#### Extracting Version Information
As an alternative to specifying the version directly in the YAML file, there are two alternatives which may be more
suitable, depending on the use case:

##### Link to an External File
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

##### Setting the Version from the Command Line
It is also possible to set the version directly over the command line using the `--version` option:
```cmd
create-version-file metadata.yml --outfile file_version_info.txt --version 0.8.1.5
```
This can be useful if you want to use a CI build number as the version. 

### Functional API
You can also use pyinstaller-versionfile from your own python code by directly calling the functional API.
``` Python
import pyinstaller_versionfile

pyinstaller_versionfile.create_versionfile_from_input_file(
    output_file="versionfile.txt",
    input_file="metadata.yml",
    version="1.2.3.4"  # optional, can be set to overwrite version information (equivalent to --version when using the CLI)
)
```

It is not necessary to use a file as input, you can also directly specify the desired values.
All of them are optional and will be filled with placeholder values if not specified.
``` Python
import pyinstaller_versionfile

pyinstaller_versionfile.create_versionfile(
    output_file="versionfile.txt",
    version="1.2.3.4",
    company_name="My Imaginary Company",
    file_description="Simple App",
    internal_name="Simple App",
    legal_copyright="© My Imaginary Company. All rights reserved.",
    original_filename="SimpleApp.exe",
    product_name="Simple App"
)
```

## Contributing

If you think you found a bug, or have a proposal for an enhancement, do not hesitate 
to create a new issue or submit a pull request. I will look into it as soon
as possible.
