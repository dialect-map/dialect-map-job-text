#!/usr/bin/env python

import click

from click import Context
from click import Path

from dialect_map_gcp.auth import OpenIDAuthenticator
from dialect_map_io.data_input import ArxivInputAPI
from dialect_map_io.data_input import LocalDataFile
from dialect_map_io.data_output import RestOutputAPI
from dialect_map_io.parsers import JSONDataParser
from dialect_map_io.parsers import PDFTextParser

from job.files import FileSystemIterator
from job.input import ApiMetadataSource
from job.input import FileMetadataSource
from job.input import PDFCorpusSource
from job.output import DialectMapOperator
from job.parsers import FeedMetadataParser
from job.parsers import JSONMetadataParser
from logs import setup_logger
from pipes import LocalTextPipeline
from pipes import MetadataPipeline


@click.group()
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
    pdf_parser = PDFTextParser()
    pdf_reader = PDFCorpusSource(pdf_parser)

    pipeline = LocalTextPipeline(files_iterator, pdf_reader)
    pipeline.run(output_files_path)


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
    "--metadata-file-path",
    help="JSON metadata file local path",
    required=False,
    type=Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
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
    "--api-url",
    help="Private API base URL",
    required=True,
    type=str,
)
def metadata_job(
    input_files_path: str,
    metadata_file_path: str,
    gcp_key_path: str,
    api_url: str,
):
    """Iterates on all PDF papers and send their metadata to the specified API"""

    # Initialize file iterator
    file_iter = FileSystemIterator(input_files_path, ".pdf")

    # Initialize API controller
    api_auth = OpenIDAuthenticator(gcp_key_path, api_url)
    api_conn = RestOutputAPI(api_url, api_auth)
    api_ctl = DialectMapOperator(api_conn)

    # Initialize metadata sources
    file_source = FileMetadataSource(
        LocalDataFile(metadata_file_path, JSONDataParser()),
        JSONMetadataParser(),
    )
    api_source = ApiMetadataSource(
        ArxivInputAPI("https://export.arxiv.org/api"),
        FeedMetadataParser(),
    )

    pipeline = MetadataPipeline(file_iter, api_ctl)
    pipeline.add_source(file_source)
    pipeline.add_source(api_source)
    pipeline.run()


if __name__ == "__main__":
    main()
