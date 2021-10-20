# -*- coding: utf-8 -*-

from typing import List

from dialect_map_schemas import CategoryMembershipSchema
from dialect_map_schemas import PaperSchema
from dialect_map_schemas import PaperAuthorSchema

from ..models import ArxivMetadata


class ArxivMetadataMapper:
    """ArXiv metadata to Dialect map records mapper"""

    @staticmethod
    def get_paper_data(metadata: ArxivMetadata) -> dict:
        """
        Adapts one of the ArXiv metadata entries into a Paper record
        :param metadata: ArXiv metadata entry
        :return: Paper record
        """

        schema = PaperSchema()
        record = schema.load(
            {
                "arxiv_id": metadata.paper_id,
                "arxiv_rev": metadata.paper_rev,
                "title": metadata.paper_title,
                "doi_id": metadata.paper_doi,
                "revision_date": metadata.paper_updated_at.date(),
                "submission_date": metadata.paper_created_at.date(),
                "created_at": metadata.paper_created_at,
                "updated_at": metadata.paper_updated_at,
            }
        )

        return schema.dump(record)

    @staticmethod
    def get_paper_authors(metadata: ArxivMetadata) -> List[dict]:
        """
        Adapts one of the ArXiv metadata entries into several PaperAuthor records
        :param metadata: ArXiv metadata entry
        :return: PaperAuthor records
        """

        shared = {
            "arxiv_id": metadata.paper_id,
            "arxiv_rev": metadata.paper_rev,
            "created_at": metadata.paper_created_at,
        }

        schemas = PaperAuthorSchema(many=True)
        records = [{"author_name": author.name, **shared} for author in metadata.paper_authors]
        records = schemas.load(records)

        return schemas.dump(records)

    @staticmethod
    def get_paper_membership(metadata: ArxivMetadata) -> dict:
        """
        Adapts one of the ArXiv metadata entries into a CategoryMembership record
        :param metadata: ArXiv metadata entry
        :return: CategoryMembership record
        """

        schema = CategoryMembershipSchema()
        record = schema.load(
            {
                "arxiv_id": metadata.paper_id,
                "arxiv_rev": metadata.paper_rev,
                "category_id": metadata.paper_category,
                "created_at": metadata.paper_created_at,
            }
        )

        return schema.dump(record)
