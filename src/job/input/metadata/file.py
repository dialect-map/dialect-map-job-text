# -*- coding: utf-8 -*-

import logging

from typing import List
from dialect_map_io import JSONFileHandler

from .base import BaseMetadataSource
from ...models import ArxivMetadata
from ...parsers import JSONMetadataParser

logger = logging.getLogger()


class JSONMetadataSource(BaseMetadataSource):
    """JSON file source for the metadata information"""

    def __init__(self, handler: JSONFileHandler, parser: JSONMetadataParser, file_path: str):
        """
        Initializes the metadata operator with a given JSON parser
        :param handler: local data file with the metadata to iterate on
        :param parser: object to parse the metadata entries
        :param file_path: path to the metadata file
        """

        self.handler = handler
        self.parser = parser
        self.entries = self._build_metadata_file(file_path)

    def _build_metadata_file(self, file_path: str) -> dict:
        """
        Builds an ID - JSON dictionary after iterating the provided metadata file
        :param file_path: path to the metadata file
        :return: ID - JSON dictionary
        """

        return {json["id"]: json for json in self.handler.read_items(file_path)}

    def get_metadata(self, paper_id: str) -> List[ArxivMetadata]:
        """
        Retrieves the complete metadata of the multiple ArXiv paper versions
        :param paper_id: ArXiv paper ID
        :return: ArXiv paper versions metadata
        """

        meta = []

        try:
            json = self.entries[paper_id]
        except KeyError:
            logger.error(f"Paper {paper_id} not found in the ArXiv metadata file")
        else:
            meta = self.parser.parse_body(json)

        return meta
