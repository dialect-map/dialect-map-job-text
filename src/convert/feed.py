# -*- coding: utf-8 -*-

from typing import List

from dialect_map_io import ArxivFeedEntry
from dialect_map_schemas import CategoryMembershipSchema
from dialect_map_schemas import PaperSchema
from dialect_map_schemas import PaperAuthorSchema


class ArxivFeedConverter:
    """ArXiv feed to Dialect map records converter"""

    @staticmethod
    def get_paper_data(feed_entry: ArxivFeedEntry) -> dict:
        """
        Adapts one of the ArXiv feed entry information into a Paper record
        :param feed_entry: ArXiv feed entry information
        :return: Paper record
        """

        schema = PaperSchema()
        record = schema.load(
            {
                "arxiv_id": feed_entry.paper_id,
                "arxiv_rev": feed_entry.paper_rev,
                "title": feed_entry.paper_title,
                "doi_id": feed_entry.paper_doi,
                "revision_date": feed_entry.paper_updated_at.date(),
                "submission_date": feed_entry.paper_created_at.date(),
                "created_at": feed_entry.paper_created_at,
                "updated_at": feed_entry.paper_updated_at,
            }
        )

        return schema.dump(record)

    @staticmethod
    def get_paper_authors(feed_entry: ArxivFeedEntry) -> List[dict]:
        """
        Adapts one of the ArXiv feed entry information into several PaperAuthor records
        :param feed_entry: ArXiv feed entry information
        :return: PaperAuthor records
        """

        shared = {
            "arxiv_id": feed_entry.paper_id,
            "arxiv_rev": feed_entry.paper_rev,
            "created_at": feed_entry.paper_created_at,
        }

        schemas = PaperAuthorSchema(many=True)
        records = [{"author_name": author.name, **shared} for author in feed_entry.paper_authors]
        records = schemas.load(records)

        return schemas.dump(records)

    @staticmethod
    def get_paper_membership(feed_entry: ArxivFeedEntry) -> dict:
        """
        Adapts one of the ArXiv feed entry information into a CategoryMembership record
        :param feed_entry: ArXiv feed entry information
        :return: CategoryMembership record
        """

        schema = CategoryMembershipSchema()
        record = schema.load(
            {
                "arxiv_id": feed_entry.paper_id,
                "arxiv_rev": feed_entry.paper_rev,
                "category_id": feed_entry.paper_category,
                "created_at": feed_entry.paper_created_at,
            }
        )

        return schema.dump(record)
