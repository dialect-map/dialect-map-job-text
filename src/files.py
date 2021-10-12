# -*- coding: utf-8 -*-

import glob

from pathlib import Path
from typing import Generator
from typing import List


class FileSystemIterator:
    """File system iterator for file system trees"""

    def __init__(self, root_path: str, extension: str):
        """
        Initializes a File System iterator to traverse the tree
        :param root_path: root file path to iterator from
        :param extension: file extensions to accept
        """

        self.root_path = Path(root_path).resolve()
        self.glob_path = f"{self.root_path}/**/*{extension}"

    @staticmethod
    def get_file_name(path: str) -> str:
        """
        Extracts a file name out of a path
        :param path: complete file path
        :return: file name
        """

        return Path(path).name

    @staticmethod
    def get_node_name(path: str, node_index: int) -> str:
        """
        Extracts a path node from the complete path
        :param path: complete file path
        :param node_index: node index to extract
        :return: path node
        """

        return Path(path).parts[node_index]

    def all_paths(self) -> List[str]:
        """
        Returns a list of absolute paths for the matched files
        :return: list of absolute paths
        """

        return glob.glob(self.glob_path, recursive=True)

    def iter_paths(self) -> Generator:
        """
        Returns an absolute path to one of the matching files
        :return: absolute path
        """

        for path in glob.iglob(self.glob_path, recursive=True):
            yield path
