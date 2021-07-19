# -*- coding: utf-8 -*-

import logging

from dialect_map_io import RestOutputAPI

logger = logging.getLogger()


class DialectMapOperator:
    """Class to operate on the Dialect map API"""

    def __init__(self, api_object: RestOutputAPI):
        """
        Initializes the Dialect map API operator object
        :param api_object: Dialect map API instantiated object
        """

        self.api_object = api_object

    def create_record(self, api_path: str, record: dict) -> None:
        """
        Creates the given record on the specified API path
        :param api_path: API path to send the data
        :param record: data record to send
        """

        try:
            self.api_object.create_record(api_path, record)
        except Exception as error:
            logger.error(f"Cannot create record: {record}")
            logger.error(f"Error: {error}")
            raise

    def archive_record(self, api_path: str, record_id: str) -> None:
        """
        Archives an existing record on the specified API path
        :param api_path: API path to patch
        :param record_id: record ID to patch
        """

        try:
            self.api_object.archive_record(f"{api_path}/{record_id}")
        except Exception as error:
            logger.error(f"Cannot archive record with ID: {record_id}")
            logger.error(f"Error: {error}")
            raise
