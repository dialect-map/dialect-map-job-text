#!/usr/bin/env python

import click
import logging

from click import Context
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


if __name__ == "__main__":
    main()
