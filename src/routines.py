# -*- coding: utf-8 -*-

import asyncio
import logging

from abc import ABC
from abc import abstractmethod
from typing import List
from urllib.parse import urlparse

from dialect_map_io.handlers import TextFileHandler
from dialect_map_io.handlers import init_handler_cls
from dialect_map_schemas.routes import DM_PAPER_METADATA_ROUTE

from job.files import FileSystemIterator
from job.input import PDFCorpusSource
from job.input import init_source_cls
from job.models import ArxivMetadata
from job.output import DialectMapOperator
from job.output import LocalFileOperator

logger = logging.getLogger()


class BaseRoutine(ABC):
    """Base class for the job routines"""

    @abstractmethod
    def run(self, destination_path: str) -> None:
        """
        Main routine to move data from a source to a destination
        :param destination_path: output path to save the data
        """

        raise NotImplementedError()


class LocalTextRoutine(BaseRoutine):
    """Routine extracting local ArXiv corpus texts"""

    def __init__(self, file_iter: FileSystemIterator, pdf_source: PDFCorpusSource):
        """
        Initializes the local ArXiv corpus text extraction routine
        :param file_iter: Local file system iterator
        :param pdf_source: PDF file corpus source
        """

        self.file_iter = file_iter
        self.pdf_source = pdf_source

    def run(self, destination_path: str) -> None:
        """
        Main routine to extract ArXiv corpus text and store it locally
        :param destination_path: output folder to save the plain texts
        """

        for file_path in self.file_iter.iter_paths():
            file_name = self.file_iter.get_file_name(file_path)
            path_diff = self.file_iter.get_path_diff(file_path)
            output_path = f"{destination_path}/{path_diff}"

            # Initialize TXT file writer
            txt_handler = TextFileHandler()
            txt_operator = LocalFileOperator(output_path, txt_handler)

            # Save paper contents
            txt_content = self.pdf_source.extract_txt(file_path)
            txt_operator.write_text(file_name, txt_content)


class MetadataRoutine(BaseRoutine):
    """Routine extracting ArXiv metadata"""

    def __init__(self, file_iter: FileSystemIterator, api_ctl: DialectMapOperator):
        """
        Initializes the ArXiv corpus metadata extraction routine
        :param file_iter: Local file system iterator
        :param api_ctl: API REST operator to be used as output
        """

        self.files_iterator = file_iter
        self.api_controller = api_ctl
        self.sources = []  # type: ignore

    async def _dispatch_records(self, records: List[ArxivMetadata]) -> None:
        """
        Dispatch metadata records to the destination API
        :param records: Paper metadata records
        """

        func = self.api_controller.create_record
        route = DM_PAPER_METADATA_ROUTE

        async with asyncio.TaskGroup() as group:
            for record in records:
                group.create_task(func(route, record.paper_metadata))

    def _get_metadata_records(self, paper_id: str) -> List[ArxivMetadata]:
        """
        Gets the metadata records from the sources given an ArXiv paper ID
        :param paper_id: ArXiv paper metadata to get
        :return: list of ArXiv paper metadata records
        """

        metadata_records = []

        for source in self.sources:
            metadata_records = source.get_metadata(paper_id)
            if len(metadata_records) > 0:
                break

        return metadata_records

    def add_sources(self, metadata_urls: List[str]) -> None:
        """
        Adds an ArXiv metadata source to the list of sources
        :param metadata_urls: URLs to extract ArXiv metadata from
        """

        for url in metadata_urls:
            url_obj = urlparse(url)
            handler = init_handler_cls(url_obj)
            source = init_source_cls(url_obj, handler)

            self.sources.append(source)

    def run(self, *args) -> None:
        """
        Main routine to extract ArXiv corpus metadata and send it to a REST API
        :param args: placeholder for positional arguments (avoid MyPy errors)
        """

        for file_path in self.files_iterator.iter_paths():
            file_name = self.files_iterator.get_file_name(file_path)
            records = self._get_metadata_records(file_name)

            if len(records) == 0:
                logger.warning(f"Metadata for paper {file_name} not found")
                continue

            asyncio.run(self._dispatch_records(records))
