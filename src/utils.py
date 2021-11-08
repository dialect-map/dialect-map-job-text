# -*- coding: utf-8 -*-

from typing import List

from dialect_map_gcp.auth import OpenIDAuthenticator
from dialect_map_io.data_input import ArxivInputAPI
from dialect_map_io.data_input import LocalDataFile
from dialect_map_io.data_output import RestOutputAPI
from dialect_map_io.parsers import JSONDataParser

from job.input import BaseMetadataSource
from job.input import ApiMetadataSource
from job.input import FileMetadataSource
from job.output import DialectMapOperator
from job.parsers import FeedMetadataParser
from job.parsers import JSONMetadataParser


def init_api_operator(api_url: str, key_path: str) -> DialectMapOperator:
    """
    Initializes the Dialect map API operator
    :param api_url: Dialect map API base URL
    :param key_path: Service Account key path
    :return: initialized API operator
    """

    api_auth = OpenIDAuthenticator(key_path, api_url)
    api_conn = RestOutputAPI(api_url, api_auth)

    return DialectMapOperator(api_conn)


def init_metadata_sources(metadata_file_path: str = None) -> List[BaseMetadataSource]:
    """
    Initializes a list of ArXiv metadata sources in order of preference
    :param metadata_file_path: path to the ArXiv metadata JSON file
    :return: list of initialized metadata sources
    """

    # Initialize metadata parsing objects
    metadata_feed_parser = FeedMetadataParser()
    metadata_json_parser = JSONMetadataParser()

    # Initialize data parsing objects
    json_parser = JSONDataParser()

    return [
        FileMetadataSource(
            LocalDataFile(metadata_file_path, json_parser),
            metadata_json_parser,
        ),
        ApiMetadataSource(
            ArxivInputAPI("https://export.arxiv.org/api"),
            metadata_feed_parser,
        ),
    ]
