# -*- coding: utf-8 -*-

from typing import List

from dialect_map_io import ArxivInputAPI

from .base import BaseMetadataSource
from ...models import ArxivMetadata
from ...parsers import FeedMetadataParser


class ApiMetadataSource(BaseMetadataSource):
    """Metadata operator for the ArXiv feed API"""

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

        feed = self.api.request_paper(paper_id)
        meta = self.parser.parse_body(feed)

        return meta
