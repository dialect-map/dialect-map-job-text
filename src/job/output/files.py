# -*- coding: utf-8 -*-

import logging

from pathlib import Path
from dialect_map_io import BaseFileHandler

logger = logging.getLogger()


class LocalFileOperator:
    """Class to write on local file system files"""

    def __init__(self, destination: str, file_handler: BaseFileHandler):
        """
        Initializes the local file system operator object
        :param destination: folder to create the files
        :param file_handler: file to dump the content
        """

        self.destination = destination
        self.file_handler = file_handler

    def _build_path(self, file_name: str) -> Path:
        """
        Builds the complete path where the file will be created
        :param file_name: file name
        :return: complete file path
        """

        return Path(self.destination, file_name)

    def write_text(self, file_name: str, text: str) -> None:
        """
        Writes the given text into the desired file name
        :param file_name: name for the output file
        :param text: content for the output file
        """

        file_path = self._build_path(file_name)

        if not file_path.exists():
            logging.warning(f"File {file_path} already exists")
            return

        self.file_handler.write_file(
            file_path=str(file_path),
            content=text,
        )
