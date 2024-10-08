# -*- coding: utf-8 -*-

import logging
import re

from typing import List
from typing import override
from urllib import parse

from feedparser import FeedParserDict
from feedparser import parse as feed_parse

from .base import BaseMetadataParser
from ..models import ArxivMetadata
from ..models import ArxivMetadataAuthor
from ..models import ArxivMetadataCategory
from ..models import ArxivMetadataLink

logger = logging.getLogger()


class FeedMetadataParser(BaseMetadataParser):
    """
    Class implementing the Atom 1.0 parsing functionality for the ArXiv feed
    Atom reference: https://www.ietf.org/rfc/rfc4287.txt
    ArXiv feed: https://arxiv.org/help/api/user-manual#52-details-of-atom-results-returned
    """

    def __init__(self):
        """Initializes the ArXiv feed metadata parser object"""

        self.entry_id_prefix = re.compile(r"http://arxiv.org/abs/")
        self.entry_id_suffix = re.compile(r"v\d+")
        self.entry_rev_regex = re.compile(r"v(\d+)")

    @staticmethod
    def _parse_links(link_entries: list) -> List[str]:
        """
        Parses and extracts a link href attributes from the feed
        :param link_entries: list encapsulating current level links
        :return: link URLs
        """

        return [parse.unquote(link.href) for link in link_entries]

    def _extract_id(self, entry_id: str) -> str:
        """
        Extract the paper ID from the value found on the <entry>.<id> field
        :param entry_id: value found on <entry>.<id>
        :return: paper ID
        """

        id = entry_id
        id = re.sub(self.entry_id_prefix, "", id, count=1)
        id = re.sub(self.entry_id_suffix, "", id, count=1)
        return id

    def _extract_rev(self, entry_id: str) -> int:
        """
        Extract the paper revision from the value found on the <entry>.<id> field
        :param entry_id: value found on <entry>.<id>
        :return: paper revision
        """

        rev = re.search(self.entry_rev_regex, entry_id)
        rev = rev.group(1) if rev is not None else 1

        return int(rev)

    def _extract_doi(self, entry: FeedParserDict) -> str:
        """
        Extract the paper DOI from the value found on the <entry> structure
        :param entry: feed <entry> structure
        :return: paper DOI
        """

        try:
            paper_doi = entry.arxiv_doi
        except AttributeError:
            paper_doi = ""
            paper_id = self._extract_id(entry.id)
            logger.info(f"Paper {paper_id} does not specify a DOI")

        return paper_doi

    @override
    def parse_body(self, feed: str) -> List[ArxivMetadata]:
        """
        Parses the body section of a given feed API result
        :param feed: metadata string for a given paper
        :return: parsed metadata objects
        """

        papers = []
        parsed = feed_parse(feed)

        for entry in parsed.entries:
            categos = [ArxivMetadataCategory(tag.term) for tag in entry.tags]
            authors = [ArxivMetadataAuthor(author.name) for author in entry.authors]
            links = [ArxivMetadataLink(l["href"], l["type"]) for l in entry.links]

            paper = ArxivMetadata(
                paper_id=self._extract_id(entry.id),
                paper_rev=self._extract_rev(entry.id),
                paper_doi=self._extract_doi(entry),
                paper_title=self._parse_string(entry.title),
                paper_description=self._parse_string(entry.summary),
                paper_categories=categos,
                paper_authors=authors,
                paper_links=links,
                paper_created_at=self._parse_date(entry.published),
                paper_updated_at=self._parse_date(entry.updated),
            )

            papers.append(paper)

        return papers
