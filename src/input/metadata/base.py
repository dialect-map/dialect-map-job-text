# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from typing import List

from dialect_map_io import ArxivFeedEntry


class BaseMetadataSource(ABC):
    """Interface for the metadata sources"""

    @abstractmethod
    def get_metadata(self, paper_id: str) -> List[ArxivFeedEntry]:
        """
        Retrieves the complete metadata of the multiple ArXiv paper versions
        :param paper_id: ArXiv paper ID
        :return: ArXiv paper versions metadata
        """

        raise NotImplementedError()
