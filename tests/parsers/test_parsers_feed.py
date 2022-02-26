# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from datetime import time
from datetime import timezone

import pytest

from src.job.models import ArxivMetadata
from src.job.models import ArxivMetadataAuthor
from src.job.models import ArxivMetadataCategory
from src.job.models import ArxivMetadataLink
from src.job.parsers import FeedMetadataParser

from ..__paths import FEED_FOLDER


@pytest.fixture(scope="module")
def feed_entry() -> ArxivMetadata:
    """
    Feed entry object parsed from a sample Arxiv Atom feed
    :return: feed entry object
    """

    feed_parser = FeedMetadataParser()

    feed_file = FEED_FOLDER.joinpath("arxiv_feed.xml")
    feed_text = open(feed_file, "r").read()
    feed_objs = feed_parser.parse_body(feed_text)

    return feed_objs[0]


def test_feed_entries_parse(feed_entry: ArxivMetadata):
    """
    Tests the correct parsing of the Arxiv feed entries fields
    :param feed_entry: feed entry object
    """

    assert feed_entry.paper_id == "hep-ex/0307015"
    assert feed_entry.paper_rev == 1
    assert feed_entry.paper_doi == "10.1140/epjc/s2003-01326-x"
    assert feed_entry.paper_title == (
        "Multi-Electron Production at High Transverse Momenta in ep Collisions at HERA"
    )

    assert feed_entry.paper_description == (
        "Multi-electron production is studied at high electron transverse momentum in "
        "positron- and electron-proton collisions using the H1 detector at HERA. The "
        "data correspond to an integrated luminosity of 115 pb-1. Di-electron and "
        "tri-electron event yields are measured."
    )

    assert feed_entry.paper_created_at == datetime.combine(
        date=date(2003, 7, 7),
        time=time(17, 46, 40),
        tzinfo=timezone.utc,
    )

    assert feed_entry.paper_updated_at == datetime.combine(
        date=date(2003, 7, 7),
        time=time(17, 46, 40),
        tzinfo=timezone.utc,
    )


def test_feed_entries_authors_parse(feed_entry: ArxivMetadata):
    """
    Tests the correct parsing of the Arxiv feed authors field
    :param feed_entry: feed entry object
    """

    assert feed_entry.paper_authors == [
        ArxivMetadataAuthor("H1 Collaboration"),
    ]


def test_feed_entries_categories_parse(feed_entry: ArxivMetadata):
    """
    Tests the correct parsing of the Arxiv feed categories field
    :param feed_entry: feed entry object
    """

    assert feed_entry.paper_categories == [
        ArxivMetadataCategory("hep-ex"),
    ]


def test_feed_entries_links_parse(feed_entry: ArxivMetadata):
    """
    Tests the correct parsing of the Arxiv feed link fields
    :param feed_entry: feed entry object
    """

    assert feed_entry.paper_links == [
        ArxivMetadataLink("http://dx.doi.org/10.1140/epjc/s2003-01326-x", "text/html"),
        ArxivMetadataLink("http://arxiv.org/abs/hep-ex/0307015v1", "text/html"),
        ArxivMetadataLink("http://arxiv.org/pdf/hep-ex/0307015v1", "application/pdf"),
    ]
