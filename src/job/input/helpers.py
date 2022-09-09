# -*- coding: utf-8 -*-

from urllib.parse import ParseResult

from dialect_map_io import BaseHandler
from dialect_map_io import ArxivAPIHandler
from dialect_map_io import JSONFileHandler

from .metadata import *
from ..parsers import FeedMetadataParser
from ..parsers import JSONMetadataParser


SOURCE_TYPE_API = "api"
SOURCE_TYPE_FILE = "file"

SOURCE_TYPE_MAPPINGS = {
    SOURCE_TYPE_API: {
        "handler_cls": ArxivAPIHandler,
        "parser_cls": FeedMetadataParser,
        "source_cls": ArxivMetadataSource,
    },
    SOURCE_TYPE_FILE: {
        "handler_cls": JSONFileHandler,
        "parser_cls": JSONMetadataParser,
        "source_cls": JSONMetadataSource,
    },
}


def init_source_cls(url: ParseResult, handler: BaseHandler) -> BaseMetadataSource:
    """
    Returns a source class depending on the provided URL
    :param url: parsed URL to initialize the source for
    :param handler: handler to get the metadata from
    :return: source instance
    """

    match url.scheme:
        case "file":
            classes = SOURCE_TYPE_MAPPINGS[SOURCE_TYPE_FILE]
            kwargs = {"file_path": url.path}
        case "http" | "https":
            classes = SOURCE_TYPE_MAPPINGS[SOURCE_TYPE_API]
            kwargs = {}
        case _:
            raise ValueError("Source not specified for the provided URL")

    handler_cls = classes["handler_cls"]
    parser_cls = classes["parser_cls"]
    source_cls = classes["source_cls"]

    assert isinstance(handler, handler_cls)
    return source_cls(handler=handler, parser=parser_cls(), **kwargs)
