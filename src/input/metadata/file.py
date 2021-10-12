# -*- coding: utf-8 -*-

from typing import List

from dialect_map_io import ArxivFeedEntry
from dialect_map_io import JSONDataParser

from .base import BaseMetadataSource


class FileMetadataSource(BaseMetadataSource):
    """Metadata source for the ArXiv JSON file"""

    def __init__(self, file_path: str, parser: JSONDataParser):
        """
        Initializes the metadata operator with a given JSON parser
        :param file_path: path to the metadata JSON file
        :param parser: object to parse the metadata entries
        """

        self.parser = parser
        self.entries = self._parse_metadata_file(file_path)

    def _parse_metadata_file(self, file_path: str) -> dict:
        """
        Parses the provided metadata file building a ID - JSON dictionary
        :param file_path: path to the metadata JSON file
        :return: ID - JSON dictionary
        """

        entries = {}

        with open(file_path) as file:

            for line in file.readlines():
                json = self.parser.parse_str(line)
                assert isinstance(json, dict)

                key = json["id"]
                val = json
                entries[key] = val

        return entries

    def get_metadata(self, paper_id: str) -> List[ArxivFeedEntry]:
        """
        Retrieves the complete metadata of the multiple ArXiv paper versions
        :param paper_id: ArXiv paper ID
        :return: ArXiv paper versions metadata
        """

        pass
