# Contributing

## Installing the project

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. 
Therefore, Poetry should be [installed](https://python-poetry.org/docs/main/#installation) on your local machine.

To install requirements, in the root directory, run:

```bash
poetry install
```

## Running tests

This project uses [tox](https://tox.wiki/en/stable/) for testing.

For linting checks, run:

```bash
tox -e lint
```

For unit tests, run:

```bash
tox -e tests
```

To include the end-to-end tests on Windows, set the environment variable `includeE2E` to `true` and run:

```bash
tox -e tests-win
```

## Changelog

Currently, the changelog is maintained manually.
