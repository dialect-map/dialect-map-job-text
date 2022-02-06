# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod

from dialect_map_io.data_output import TextFileWriter

from job.files import FileSystemIterator
from job.input import PDFCorpusSource
from job.output import LocalFileOperator


class BasePipeline(ABC):
    """Base class for the job pipelines"""

    @abstractmethod
    def run(self, destination_path: str) -> None:
        """
        Main routine to move data from a source to a destination
        :param destination_path: output path to save the data
        """

        raise NotImplementedError()


class LocalTextPipeline(BasePipeline):
    """Pipeline extracting local ArXiv corpus texts"""

    def __init__(self, file_iter: FileSystemIterator, pdf_reader: PDFCorpusSource):
        """
        Initializes the local ArXiv corpus text extraction pipeline
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
