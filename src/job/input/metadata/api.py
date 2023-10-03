# -*- coding: utf-8 -*-

import logging

from typing import List
from typing import override
from dialect_map_io import ArxivAPIHandler

from .base import BaseMetadataSource
from ...models import ArxivMetadata
from ...parsers import FeedMetadataParser

logger = logging.getLogger()


class ArxivMetadataSource(BaseMetadataSource):
    """ArXiv API source for the metadata information"""

    def __init__(self, handler: ArxivAPIHandler, parser: FeedMetadataParser):
        """
        Initializes the metadata operator with a given API and parser
        :param handler: object to retrieve the ArXiv metadata feed
        :param parser: object to parse the ArXiv metadata feed
        """

        self.handler = handler
        self.parser = parser

    @override
    def get_metadata(self, paper_id: str) -> List[ArxivMetadata]:
        """
        Retrieves the complete metadata of the multiple ArXiv paper versions
        :param paper_id: ArXiv paper ID
        :return: ArXiv paper versions metadata
        """

        meta = []

        try:
            feed = self.handler.request_metadata(paper_id)
        except ConnectionError:
            logger.error(f"Paper {paper_id} not found in the ArXiv export API")
        else:
            meta = self.parser.parse_body(feed)

        return meta
