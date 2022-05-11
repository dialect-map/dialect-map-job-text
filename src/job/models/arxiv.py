# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable
from typing import List

from dialect_map_schemas import CategoryMembershipSchema
from dialect_map_schemas import PaperSchema
from dialect_map_schemas import PaperAuthorSchema
from dialect_map_schemas import PaperMetadataSchema


@dataclass
class ArxivMetadataAuthor:
    """
    Object containing the author field of an Arxiv metadata entry

    :attr name: name of the author
    """

    name: str


@dataclass
class ArxivMetadataCategory:
    """
    Object containing the category field of an Arxiv metadata entry

    :attr name: name of the category
    """

    name: str


@dataclass
class ArxivMetadataLink:
    """
    Object containing the link fields of an Arxiv metadata entry

    :attr resource_url: resource URL assigned to the provided link
    :attr resource_type: resource type assigned to the provided link
    """

    resource_url: str
    resource_type: str


@dataclass
class ArxivMetadata:
    """
    Object containing the fields of an Arxiv metadata entry

    :attr paper_id: unique identifier
    :attr paper_rev: unique revision
    :attr paper_doi: DOI identifier
    :attr paper_title: paper title
    :attr paper_description: paper description
    :attr paper_categories: categories list
    :attr paper_authors: authors list
    :attr paper_links: resources links list
    :attr paper_created_at: paper submission date
    :attr paper_updated_at: paper updated date (same as created in revision #1)
    """

    paper_id: str
    paper_rev: int
    paper_doi: str
    paper_title: str
    paper_description: str
    paper_categories: List[ArxivMetadataCategory]
    paper_authors: List[ArxivMetadataAuthor]
    paper_links: List[ArxivMetadataLink]
    paper_created_at: datetime
    paper_updated_at: datetime

    @property
    def paper_metadata(self) -> dict:
        """Adapts the ArXiv metadata object into a PaperMetadata record"""

        schema = PaperMetadataSchema()

        return {
            schema.paper.name: self._build_paper_record(),
            schema.authors.name: self._build_author_records(),
            schema.memberships.name: self._build_membership_records(),
        }

    def _build_paper_record(self) -> dict:
        """Builds an ArXiv paper dictionary out of the ArXiv metadata object"""

        schema = PaperSchema()

        return {
            schema.arxiv_id.name: self.paper_id,
            schema.arxiv_rev.name: self.paper_rev,
            schema.title.name: self.paper_title,
            schema.doi_id.name: self.paper_doi,
            schema.revision_date.name: self.paper_updated_at.date().isoformat(),
            schema.submission_date.name: self.paper_created_at.date().isoformat(),
            schema.created_at.name: self.paper_created_at.isoformat(),
            schema.updated_at.name: self.paper_updated_at.isoformat(),
        }

    def _build_author_records(self) -> Iterable[dict]:
        """Builds an ArXiv author dictionary out of the ArXiv metadata object"""

        schema = PaperAuthorSchema()

        for author in self.paper_authors:
            yield {
                schema.arxiv_id.name: self.paper_id,
                schema.arxiv_rev.name: self.paper_rev,
                schema.author_name.name: author.name,
                schema.created_at.name: self.paper_created_at.isoformat(),
            }

    def _build_membership_records(self) -> Iterable[dict]:
        """Builds an ArXiv category membership dictionary out of the ArXiv metadata object"""

        schema = CategoryMembershipSchema()

        for category in self.paper_categories:
            yield {
                schema.arxiv_id.name: self.paper_id,
                schema.arxiv_rev.name: self.paper_rev,
                schema.category_id.name: category.name,
                schema.created_at.name: self.paper_created_at.isoformat(),
            }
