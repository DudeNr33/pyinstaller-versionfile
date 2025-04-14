# Changelog

## v3.0.1 (2025-04-14)

### New

* Provide type information and add `py.typed` file. [DudeNr33]

## v3.0.0 (2024-11-04)

### New

* Drop compatibility with Python <3.9 [DudeNr33]

* New option to extract information from distribution metadata instead of YAML file. [truderung]

* New CLI parameter `--source-format` with possible values `yaml`, `distribution`, `dist` to select the source for metadata. [truderung]

* New CLI command `--pyivf-make_version` with greater flexibility - you can specify all options via command line options (without needing a YAML file),
or overwrite any of the parameters provided in the input file or distribution metadata. [DudeNr33]

### Internal

* Switch to Poetry for packaging.

* Remove gitchangelog for changelog generation, as it would require a rewrite of the git history. Changelog is maintained manually.

## v2.1.1 (2022-11-21)

### Fix

* Add new `translations` parameter to functional API. [DudeNr33]

## v2.1.0 (2022-11-20)

### New

* Add support for *Translation* field to specify supported languages and charsets. [DudeNr33]

* Added a table with the official definition of the parameters in the Readme. [mkhoshbin1]

## v2.0.0 (2021-04-06)

### New

* Functional API for programmatic use. [DudeNr33]

* Drop compatibility with Python<3.6. [DudeNr33]

* Definition of metadata and creation of version file are now handled in separate classes, and it is not strictly necessary to use a file as input. [DudeNr33]

* Use gitchangelog for automatic changelog generation. [DudeNr33]
