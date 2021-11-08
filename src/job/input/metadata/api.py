# -*- coding: utf-8 -*-

import logging

from typing import List
from dialect_map_io import ArxivInputAPI

from .base import BaseMetadataSource
from ...models import ArxivMetadata
from ...parsers import FeedMetadataParser

logger = logging.getLogger()


class ApiMetadataSource(BaseMetadataSource):
    """ArXiv API source for the metadata information"""

    def __init__(self, api: ArxivInputAPI, parser: FeedMetadataParser):
        """
        Initializes the metadata operator with a given API and parser
        :param api: object to retrieve the ArXiv metadata feed
        :param parser: object to parse the ArXiv metadata feed
        """

        self.api = api
        self.parser = parser

    def get_metadata(self, paper_id: str) -> List[ArxivMetadata]:
        """
        Retrieves the complete metadata of the multiple ArXiv paper versions
        :param paper_id: ArXiv paper ID
        :return: ArXiv paper versions metadata
        """

        meta = []

        try:
            feed = self.api.request_paper(paper_id)
        except ConnectionError:
            logger.error(f"Paper {paper_id} not found in the ArXiv export API")
        else:
            meta = self.parser.parse_body(feed)

        return meta
