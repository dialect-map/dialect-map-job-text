# -*- coding: utf-8 -*-

from urllib.request import Request as URI

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


def init_source_cls(uri: URI, handler: BaseHandler) -> BaseMetadataSource:
    """
    Returns a source class depending on the provided URI
    :param uri: URI to get the source class from
    :param handler: handler to get the metadata from
    :return: source class
    """

    match uri.type:
        case "file":
            classes = SOURCE_TYPE_MAPPINGS[SOURCE_TYPE_FILE]
            kwargs = {"file_path": uri.selector}
        case "http" | "https":
            classes = SOURCE_TYPE_MAPPINGS[SOURCE_TYPE_API]
            kwargs = {}
        case _:
            raise ValueError("Source not specified for the provided URI")

    handler_cls = classes["handler_cls"]
    parser_cls = classes["parser_cls"]
    source_cls = classes["source_cls"]

    assert isinstance(handler, handler_cls)
    return source_cls(handler=handler, parser=parser_cls(), **kwargs)
