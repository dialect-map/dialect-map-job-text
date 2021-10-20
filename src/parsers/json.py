# -*- coding: utf-8 -*-

import logging
import pytz
import re

from datetime import datetime
from typing import List

from .base import BaseMetadataParser
from ..models import ArxivMetadata
from ..models import ArxivMetadataAuthor

logger = logging.getLogger()


class JSONMetadataParser(BaseMetadataParser):
    """
    Class implementing the JSON parsing functionality for the ArXiv JSON-based metadata
    Kaggle reference: https://www.kaggle.com/Cornell-University/arxiv
    """

    def __init__(self):
        """Initializes the Arxiv json metadata parser object"""

        self.entry_dt_format = "%a, %d %b %Y %H:%M:%S %Z"
        self.entry_rev_regex = re.compile(r"v(\d+)")

    @staticmethod
    def _parse_authors(author_entries: list) -> List[str]:
        """
        Parses and extracts an author complete name from each author entry
        :param author_entries: list of author info expressed as lists of strings.
        :return: author complete names
        """

        author_first_names = (entry[0] for entry in author_entries)
        author_last_names = (entry[1] for entry in author_entries)

        return [
            f"{first_name} {last_name}"
            for first_name, last_name in zip(author_first_names, author_last_names)
        ]

    def _extract_date(self, date: str) -> datetime:
        """
        Parses a date string to a UTC datetime object
        :param date: string date to parse
        :return: UTC datetime object
        """

        # Extracting the timezone out of the string
        dt = date[:-3].strip()
        tz = date[-3:].strip()

        # Pruning the timezone out of the format
        fmt = self.entry_dt_format[:-3]

        off_date = datetime.strptime(dt, fmt)
        off_date = off_date.replace(tzinfo=pytz.timezone(tz))
        utc_date = self._parse_date(off_date.isoformat())

        return utc_date

    def _extract_rev(self, version: str) -> int:
        """
        Extract the paper revision from the value found on the versions field
        :param version: value found in the versions field
        :return: paper revision
        """

        rev = re.search(self.entry_rev_regex, version)
        rev = rev.group(1) if rev is not None else 1

        return int(rev)

    def _extract_doi(self, entry: dict) -> str:
        """
        Extract and logs the paper DOI from the value found on the JSON entry
        :param entry: value found in the JSON entry
        :return: paper DOI
        """

        paper_doi = entry["doi"]

        if paper_doi is None:
            paper_doi = ""
            paper_id = entry["id"]
            logger.info(f"Paper {paper_id} does not specify a DOI")

        return paper_doi

    def parse_body(self, entry: dict) -> List[ArxivMetadata]:
        """
        Parses the metadata fields of a given metadata JSON entry
        :param entry: metadata fields of a given paper
        :return: parsed metadata objects
        """

        papers = []
        created = None

        for version in entry["versions"]:
            categories = entry["categories"].split()
            created = self._extract_date(version["created"]) if created is None else created
            updated = self._extract_date(version["created"])
            authors = [ArxivMetadataAuthor(a) for a in self._parse_authors(entry["authors_parsed"])]
            links = []  # type: ignore

            paper = ArxivMetadata(
                paper_id=entry["id"],
                paper_rev=self._extract_rev(version["version"]),
                paper_title=self._parse_string(entry["title"]),
                paper_description=self._parse_string(entry["abstract"]),
                paper_doi=self._extract_doi(entry),
                paper_category=categories[0],
                paper_authors=authors,
                paper_links=links,
                paper_created_at=created,
                paper_updated_at=updated,
            )

            papers.append(paper)

        return papers
