# -*- coding: utf-8 -*-

import logging

from abc import ABC
from abc import abstractmethod
from typing import List

from dialect_map_io.data_output import TextFileWriter
from dialect_map_schemas.routes import DM_PAPER_METADATA_ROUTE

from job.files import FileSystemIterator
from job.input import BaseMetadataSource
from job.input import PDFCorpusSource
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

    def __init__(self, file_iter: FileSystemIterator, pdf_reader: PDFCorpusSource):
        """
        Initializes the local ArXiv corpus text extraction routine
        :param file_iter: Local file system iterator
        :param pdf_reader: PDF file corpus source
        """

        self.file_iter = file_iter
        self.pdf_reader = pdf_reader

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
            txt_writer = TextFileWriter()
            txt_operator = LocalFileOperator(output_path, txt_writer)

            # Save paper contents
            txt_content = self.pdf_reader.extract_txt(file_path)
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

    def add_source(self, source: BaseMetadataSource) -> None:
        """
        Adds an ArXiv metadata source to the list of sources
        :param source: metadata source to extract ArXiv metadata from
        """

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

            for record in records:
                self.api_controller.create_record(
                    DM_PAPER_METADATA_ROUTE,
                    {
                        "paper": record.paper_record,
                        "authors": record.author_records,
                        "memberships": record.memberships_records,
                    },
                )
