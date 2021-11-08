#!/usr/bin/env python

import click
import logging

from click import Context
from click import Path
from typing import Optional

from dialect_map_io.data_output import TextFileWriter
from dialect_map_io.parsers import PDFTextParser

from job.files import FileSystemIterator
from job.input import ArxivCorpusSource
from job.mapping import ArxivMetadataMapper
from job.mapping import CATEGORY_MEMBER_ROUTE
from job.mapping import PAPER_AUTHOR_ROUTE
from job.mapping import PAPER_ROUTE
from job.output import DialectMapOperator
from job.output import LocalFileOperator
from logs import setup_logger
from utils import init_api_operator
from utils import init_metadata_sources

logger = logging.getLogger()


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

    # Initialize PDF parser and source object
    pdf_parser = PDFTextParser()
    pdf_reader = ArxivCorpusSource(pdf_parser)

    # Iterate on all files within the provided input path
    for file_path in files_iterator.iter_paths():

        # Extract output path
        path_diff = files_iterator.get_path_diff(input_files_path, file_path)
        file_name = files_iterator.get_file_name(file_path)
        output_path = f"{output_files_path}/{path_diff}"

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
