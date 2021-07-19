# -*- coding: utf-8 -*-

from typing import List

from dialect_map_io import ArxivFeedEntry
from dialect_map_io import ArxivInputAPI
from dialect_map_io import ArxivFeedParser

from .base import BaseMetadataSource


class ApiMetadataSource(BaseMetadataSource):
    """Metadata operator for the ArXiv feed API"""

    def __init__(self, api: ArxivInputAPI, parser: ArxivFeedParser):
        """
        Initializes the metadata operator with a given API and parser
        :param api: object to retrieve the ArXiv metadata feed
        :param parser: object to parse the ArXiv metadata feed
        """

        self.api = api
        self.parser = parser

    def get_metadata(self, paper_id: str) -> List[ArxivFeedEntry]:
        """
        Retrieves the complete metadata of the multiple ArXiv paper versions
        :param paper_id: ArXiv paper ID
        :return: ArXiv paper versions metadata
        """

        feed = self.api.request_paper(paper_id)
        meta = self.parser.parse_entries(feed)

        return meta
