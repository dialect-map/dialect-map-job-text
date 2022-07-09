# Dialect map: text job

[![CI/CD Status][ci-status-badge]][ci-status-link]
[![Coverage Status][cov-status-badge]][cov-status-link]
[![MIT license][mit-license-badge]][mit-license-link]
[![Code style][code-style-badge]][code-style-link]


### About
This repository contains the PDF to TXT transformation job that is run upon any new ArXiv paper.
In addition, it retrieves and sends their metadata to the [Dialect map private API][dialect-map-api]
by using one of the following sources:

- The public [ArXiv Kaggle dataset][arxiv-metadata-file].
- The public [ArXiv export API][arxiv-metadata-api].


### Dependencies
Python dependencies are specified on the multiple files within the `reqs` directory.

In order to install all the development packages, as long as the defined commit hooks:

```shell
make install-dev
```


### Formatting
All Python files are formatted using [Black][web-black], and the custom properties defined
in the `pyproject.toml` file.

```shell
make check
```


### Testing
Project testing is performed using [Pytest][web-pytest]. In order to run the tests:

```shell
make test
```


### CLI 🚀
The project contains a [main.py][main-module] module exposing a CLI with several commands:

```shell
python3 src/main.py [OPTIONS] [COMMAND] [ARGS]...
```


#### Command: `text-job`
This command starts a process that recursively traverses a file system tree of PDF files,
transforming them into their TXT equivalent.

| ARGUMENT            | ENV VARIABLE          | REQUIRED | DESCRIPTION                              |
|---------------------|-----------------------|----------|------------------------------------------|
| --input-files-path  | -                     | Yes      | Path to the list of input PDF files      |
| --output-files-path | -                     | Yes      | Path to store the output TXT files       |


#### Command: `metadata-job`
This command starts a process that recursively traverses a file system tree of PDF files,
sending their metadata to the Dialect Map _private_ API along the way. The process assumes
that each PDF is an ArXiv paper, with their names as their IDs.

| ARGUMENT            | ENV VARIABLE          | REQUIRED | DESCRIPTION                              |
|---------------------|-----------------------|----------|------------------------------------------|
| --input-files-path  | -                     | Yes      | Path to the list of input PDF files      |
| --meta-file-path    | -                     | Yes      | Path to the ArXiv metadata JSON file     |
| --gcp-key-path      | -                     | Yes      | GCP Service account key path             |
| --api-url           | -                     | Yes      | Private API base URL                     |


[ci-status-badge]: https://github.com/dialect-map/dialect-map-job-text/actions/workflows/ci.yml/badge.svg?branch=main
[ci-status-link]: https://github.com/dialect-map/dialect-map-job-text/actions/workflows/ci.yml?query=branch%3Amain
[code-style-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[code-style-link]: https://github.com/psf/black
[cov-status-badge]: https://codecov.io/gh/dialect-map/dialect-map-job-text/branch/main/graph/badge.svg
[cov-status-link]: https://codecov.io/gh/dialect-map/dialect-map-job-text
[mit-license-badge]: https://img.shields.io/badge/License-MIT-blue.svg
[mit-license-link]: https://github.com/dialect-map/dialect-map-job-text/blob/main/LICENSE

[arxiv-metadata-api]: https://arxiv.org/help/api/user-manual
[arxiv-metadata-file]: https://www.kaggle.com/Cornell-University/arxiv
[dialect-map-api]: https://github.com/dialect-map/dialect-map-private-api
[main-module]: src/main.py
[web-black]: https://black.readthedocs.io/en/stable/
[web-pytest]: https://docs.pytest.org/en/latest/#
