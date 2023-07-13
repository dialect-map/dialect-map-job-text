#!/usr/bin/env python

import click

from click import Context
from click import Path

from dialect_map_gcp.auth import OpenIDAuthenticator
from dialect_map_io.handlers import DialectMapAPIHandler
from dialect_map_io.handlers import PDFFileHandler

from job.files import FileSystemIterator
from job.input import PDFCorpusSource
from job.output import DialectMapOperator
from logs import setup_logger
from routines import LocalTextRoutine
from routines import MetadataRoutine


@click.group(cls=None)
@click.option(
    "--log-level",
    envvar="DIALECT_MAP_LOG_LEVEL",
    default="INFO",
    help="Log messages level",
    required=False,
    type=str,
)
@click.pass_context
def main(context: Context, log_level: str):
    """Default command group for the jobs"""

    setup_logger(log_level)

    params = context.ensure_object(dict)
    params["LOG_LEVEL"] = log_level


@main.command()
@click.option(
    "--input-files-path",
    help="PDF input files local path",
    required=True,
    type=Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
)
@click.option(
    "--output-files-path",
    help="TXT output files local path",
    required=True,
    type=Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
    ),
)
def text_job(input_files_path: str, output_files_path: str):
    """Iterates on all PDF papers generating TXT equivalents in the output folder"""

    # Initialize file iterator
    files_iterator = FileSystemIterator(input_files_path, ".pdf")

    # Initialize PDF reader
    pdf_handler = PDFFileHandler()
    pdf_source = PDFCorpusSource(pdf_handler)

    routine = LocalTextRoutine(files_iterator, pdf_source)
    routine.run(output_files_path)


@main.command()
@click.option(
    "--input-files-path",
    help="PDF input files local path",
    required=True,
    type=Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
)
@click.option(
    "--input-metadata-urls",
    help="URLs to the paper metadata sources",
    default=["https://export.arxiv.org/api"],
    required=False,
    multiple=True,
    type=str,
)
@click.option(
    "--gcp-key-path",
    help="GCP Service Account key path",
    required=True,
    type=Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
)
@click.option(
    "--output-api-url",
    help="Private API base URL",
    required=True,
    type=str,
)
def metadata_job(
    input_files_path: str,
    input_metadata_urls: list,
    gcp_key_path: str,
    output_api_url: str,
):
    """Iterates on all PDF papers and send their metadata to the specified API"""

    # Initialize file iterator
    file_iter = FileSystemIterator(input_files_path, ".pdf")

    # Initialize API controller
    api_auth = OpenIDAuthenticator(gcp_key_path, target_url=output_api_url)
    api_conn = DialectMapAPIHandler(api_auth, base_url=output_api_url)
    api_ctl = DialectMapOperator(api_conn)

    # Initialize and run routine
    routine = MetadataRoutine(file_iter, api_ctl)
    routine.add_sources(input_metadata_urls)
    routine.run()


if __name__ == "__main__":
    main()
