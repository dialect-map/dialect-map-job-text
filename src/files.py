# -*- coding: utf-8 -*-

import glob
import os

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

    @staticmethod
    def get_path_diff(path_a: str, path_b: str) -> Path:
        """
        Extracts the tail difference between a path and one of its sub-paths
        :param path_a: First path / sub-path to consider
        :param path_b: Second path / sub-path to consider
        :return: tail difference path
        """

        if not (path_a in path_b or path_b in path_a):
            raise ValueError("Compared paths must have some common sub-path")

        common_path_str = os.path.commonpath([path_a, path_b])
        common_path_obj = Path(common_path_str)
        common_path_len = len(common_path_obj.parts)

        path_a_parts = Path(path_a).parts
        path_b_parts = Path(path_b).parts
        longest_path = max([path_a_parts, path_b_parts], key=len)

        return Path(*longest_path[common_path_len:])

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
