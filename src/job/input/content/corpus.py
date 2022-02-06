# -*- coding: utf-8 -*-

from dialect_map_io import PDFTextParser


class PDFCorpusSource:
    """File corpus source for the PDFs content"""

    def __init__(self, parser: PDFTextParser):
        """
        Initializes the corpus operator with a given parser
        :param parser: object to parse the PDF files
        """

        self.parser = parser

    def extract_txt(self, file_path: str) -> str:
        """
        Extracts the raw text out of a PDF file
        :param file_path: path to the PDF file
        :return: file text
        """

        return self.parser.parse_file(file_path)
