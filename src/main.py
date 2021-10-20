#!/usr/bin/env python

import click
import logging

from click import Context
from click import Path
from typing import Optional

from logs import setup_logger

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

    :param context:
    :param input_files_path:
    :param output_files_path:
    :param metadata_file_path:
    :param gcp_key_path:
    :return:
    """

    pass


if __name__ == "__main__":
    main()
