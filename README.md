# Dialect map: text job

[![CI/CD Status][ci-status-badge]][ci-status-link]
[![Coverage Status][cov-status-badge]][cov-status-link]
[![MIT license][mit-license-badge]][mit-license-link]
[![Code style][code-style-badge]][code-style-link]


### About
This repository contains the PDF to TXT transformation job that is run upon any new ArXiv paper.
In addition, it can query the official ArXiv API to retrieve papers metadata.

It is used in combination with the [Dialect map IO][dialect-map-io], which provides the file parsing
and API connection capabilities, and the [Dialect map schemas][dialect-map-schemas] packages,
so the papers metadata can be sent to the [Dialect map private API][dialect-map-api].


### Dependencies
Python dependencies are specified within the `requirements.txt` and `requirements-dev.txt` files.

In order to install the development packages, as long as the defined commit hooks:
```sh
make install-dev
```


### Formatting
All Python files are formatted using [Black][web-black], and the custom properties defined
in the `pyproject.toml` file.
```sh
make check
```


### Testing
Project testing is performed using [Pytest][web-pytest]. In order to run the tests:
```sh
make test
```


### CLI 🚀
The project contains a [main.py][main-module] module exposing a CLI with several commands:
```sh
python3 src/main.py [OPTIONS] [COMMAND] [ARGS]...
```

The top-level options are:

| OPTION         | ENV VARIABLE           | DEFAULT          | REQUIRED | DESCRIPTION                              |
|----------------|------------------------|------------------|----------|------------------------------------------|
| --api-url      | DIALECT_MAP_API_URL    | -                | Yes      | Private API base URL                     |
| --log-level    | DIALECT_MAP_LOG_LEVEL  | INFO             | No       | Log messages level                       |


#### Command: `text-job`
This command starts a process that recursively traverses a file system tree of PDF files,
transforming them into their TXT equivalent, and sending metadata to the Dialect Map _private_ API along the way.
The process assumes that each PDF is an ArXiv paper, with their names as their IDs.

The command arguments are:

| ARGUMENT             | ENV VARIABLE     | DEFAULT          | REQUIRED | DESCRIPTION                              |
|----------------------|------------------|------------------|----------|------------------------------------------|
| --input-files-path   | -                | -                | Yes      | Path to the list of input PDF files      |
| --output-files-path  | -                | -                | Yes      | Path to the storage of output TXT files  |
| --metadata-file-path | -                | -                | No       | Path to the ArXiv metadata JSON file     |
| --gcp-key-path       | -                | -                | Yes      | GCP Service account key path             |


[ci-status-badge]: https://github.com/dialect-map/dialect-map-job-text/actions/workflows/ci.yml/badge.svg?branch=main
[ci-status-link]: https://github.com/dialect-map/dialect-map-job-text/actions/workflows/ci.yml?query=branch%3Amain
[code-style-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[code-style-link]: https://github.com/psf/black
[cov-status-badge]: https://codecov.io/gh/dialect-map/dialect-map-job-text/branch/main/graph/badge.svg
[cov-status-link]: https://codecov.io/gh/dialect-map/dialect-map-job-text
[mit-license-badge]: https://img.shields.io/badge/License-MIT-blue.svg
[mit-license-link]: https://github.com/dialect-map/dialect-map-job-text/blob/main/LICENSE

[dialect-map-api]: https://github.com/dialect-map/dialect-map-private-api
[dialect-map-io]: https://github.com/dialect-map/dialect-map-io
[dialect-map-schemas]: https://github.com/dialect-map/dialect-map-schemas
[web-black]: https://black.readthedocs.io/en/stable/
[web-pytest]: https://docs.pytest.org/en/latest/#
