# -*- coding: utf-8 -*-

import logging
import re

from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timezone
from typing import Any

logger = logging.getLogger()


class BaseMetadataParser(ABC):
    """Interface for the metadata parser classes"""

    @staticmethod
    def _parse_date(date_string: str) -> datetime:
        """
        Parses a date string to a UTC datetime object
        :param date_string: ArXiv date in string format
        :return: UTC datetime object
        """

        try:
            off_date = datetime.fromisoformat(date_string)
            utc_date = datetime.fromtimestamp(off_date.timestamp(), timezone.utc)
        except Exception as err:
            logger.error(err)
            raise err

        return utc_date

    @staticmethod
    def _parse_string(long_string: str) -> str:
        """
        Parses and cleans a potentially multi-line string
        :param long_string: potentially multi-line string
        :return: trimmed string
        """

        return re.sub(r"\s\s+", " ", long_string)

    @abstractmethod
    def parse_body(self, metadata: Any) -> list:
        """
        Parses the sections of a metadata record
        :param metadata: external metadata record
        :return: parsed metadata objects
        """

        raise NotImplementedError()
