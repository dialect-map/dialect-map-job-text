# -*- coding: utf-8 -*-

from typing import List

from dialect_map_io import LocalDataFile

from .base import BaseMetadataSource
from ...models import ArxivMetadata
from ...parsers import JSONMetadataParser


class FileMetadataSource(BaseMetadataSource):
    """Metadata source for the ArXiv JSON file"""

    def __init__(self, file: LocalDataFile, parser: JSONMetadataParser):
        """
        Initializes the metadata operator with a given JSON parser
        :param file: local data file with the metadata to iterate on
        :param parser: object to parse the metadata entries
        """

        self.parser = parser
        self.entries = self._build_metadata_file(file)

    @staticmethod
    def _build_metadata_file(file: LocalDataFile) -> dict:
        """
        Builds a ID - JSON dictionary after iterating the provided metadata file
        :param file: local data file with the metadata to iterate on
        :return: ID - JSON dictionary
        """

        return {json["id"]: json for json in file.iter_items()}

    def get_metadata(self, paper_id: str) -> List[ArxivMetadata]:
        """
        Retrieves the complete metadata of the multiple ArXiv paper versions
        :param paper_id: ArXiv paper ID
        :return: ArXiv paper versions metadata
        """

        json = self.entries.get(paper_id)
        meta = self.parser.parse_body(json)

        return meta
