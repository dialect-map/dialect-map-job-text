#!/usr/bin/env python

import click
import logging

from click import Context
from click import Path
from typing import Optional

from dialect_map_io.data_output import TextFileWriter
from dialect_map_io.parsers import PDFTextParser

from files import FileSystemIterator
from input import ArxivCorpusSource
from logs import setup_logger
from mapping import ArxivMetadataMapper
from mapping import CATEGORY_MEMBER_ROUTE
from mapping import PAPER_AUTHOR_ROUTE
from mapping import PAPER_ROUTE
from output import DialectMapOperator
from output import LocalFileOperator
from utils import init_api_operator
from utils import init_metadata_sources

logger = logging.getLogger()


@click.group()
@click.option(
    "--api-url",
    envvar="DIALECT_MAP_API_URL",
    help="Private API base URL",
    required=True,
    type=str,
)
@click.option(
    "--log-level",
    envvar="DIALECT_MAP_LOG_LEVEL",
    default="INFO",
    help="Log messages level",
    required=False,
    type=str,
)
@click.pass_context
def main(context: Context, api_url: str, log_level: str):
    """Default command group for the jobs"""

    setup_logger(log_level)

    params = context.ensure_object(dict)
    params["API_URL"] = api_url
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
@click.pass_context
def text_job(
    context: Context,
    input_files_path: str,
    output_files_path: str,
    metadata_file_path: Optional[str],
    gcp_key_path: str,
):
    """
    # Iterate on all PDF files within the provided file
    #   - Get metadata using files name
    #       - From file if possible
    #       - From API as a backup
    #   - Convert metadata to record dicts
    #   - Convert PDF to TXT file
    #   - Save TXT file in parallel path
    #   - Send records to Private API

    :param context:
    :param input_files_path:
    :param output_files_path:
    :param metadata_file_path:
    :param gcp_key_path:
    """

    params = context.ensure_object(dict)
    api_url = params["API_URL"]

    # Initialize file iterator and API controller
    files_iterator = FileSystemIterator(input_files_path, ".pdf")
    api_controller = init_api_operator(api_url, gcp_key_path)

    # Initialize the metadata mapper and sources
    metadata_mapper = ArxivMetadataMapper()
    metadata_sources = init_metadata_sources(metadata_file_path)

    # Iterate on all files within the provided input path
    for file_path in files_iterator.iter_paths():
        paper_id = files_iterator.get_file_name(file_path)

        # Get paper metadata
        for source in metadata_sources:
            metadata = source.get_metadata(paper_id)
            if metadata is not None:
                break
        else:
            logger.warning(f"Could not find metadata for paper: {paper_id}")
            continue

        # Extract output path
        path_diff = files_iterator.get_path_diff(input_files_path, file_path)
        file_name = files_iterator.get_file_name(file_path)
        output_path = f"{output_files_path}/{path_diff}"

        # Save paper contents
        write_contents(file_path, file_name, output_path)

        # Get records for each metadata entry
        for metadata_entry in metadata:
            dispatch_record(api_controller, metadata_mapper, metadata_entry)


def write_contents(file_path: str, file_name: str, output_path: str) -> None:
    """
    Extracts and saves the text content of a PDF into the desired output path
    :param file_path: path to the PDF file
    :param file_name: name of the PDF file
    :param output_path: path to store the TXT output
    """

    pdf_parser = PDFTextParser()
    pdf_reader = ArxivCorpusSource(pdf_parser)

    # Initialize TXT file writer
    txt_writer = LocalFileOperator(output_path, TextFileWriter())

    # Save paper contents
    txt_content = pdf_reader.extract_txt(file_path)
    txt_writer.write_text(file_name, txt_content)


def dispatch_record(api: DialectMapOperator, mapper: ArxivMetadataMapper, entry) -> None:
    """
    Dispatch metadata entry records using the provided API operator
    :param api: Dialect map API operator
    :param mapper: Dialect map schema mapper
    :param entry: metadata entry to parse
    """

    authors = mapper.get_paper_authors(entry)
    membership = mapper.get_paper_membership(entry)
    paper_info = mapper.get_paper_data(entry)

    # Send data (order matters)
    api.create_record(PAPER_ROUTE, paper_info)
    api.create_record(CATEGORY_MEMBER_ROUTE, membership)

    for author in authors:
        api.create_record(PAPER_AUTHOR_ROUTE, author)


if __name__ == "__main__":
    main()
