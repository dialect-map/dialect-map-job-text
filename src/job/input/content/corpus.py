# -*- coding: utf-8 -*-

from dialect_map_io import PDFFileHandler


class PDFCorpusSource:
    """File corpus source for the PDFs content"""

    def __init__(self, handler: PDFFileHandler):
        """
        Initializes the corpus operator with a given parser
        :param handler: object to handle PDF files
        """

        self.handler = handler

    def extract_txt(self, file_path: str) -> str:
        """
        Extracts the raw text out of a PDF file
        :param file_path: path to the PDF file
        :return: file text
        """

        return self.handler.read_file(file_path)
