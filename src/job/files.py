# -*- coding: utf-8 -*-

import glob
import os

from pathlib import Path
from typing import Generator
from typing import List
from typing import Union

StrPath = Union[str, Path]


class FileSystemIterator:
    """File system iterator for file system trees"""

    def __init__(self, root_path: StrPath, extension: str):
        """
        Initializes a File System iterator to traverse the tree
        :param root_path: root file path to iterate from
        :param extension: file extension to accept
        """

        if not Path(root_path).is_dir():
            raise ValueError("Iterator root path must be a directory")

        self.root_path = Path(root_path).resolve()
        self.glob_path = f"{self.root_path}/**/*{extension}"

    @staticmethod
    def get_file_name(path: StrPath) -> str:
        """
        Extracts a file name out of a path
        :param path: complete file path
        :return: file name
        """

        return Path(path).name

    @staticmethod
    def get_node_name(path: StrPath, node_index: int) -> str:
        """
        Extracts a path node from the complete path
        :param path: complete file path
        :param node_index: node index to extract
        :return: path node
        """

        return Path(path).parts[node_index]

    def get_path_diff(self, path: StrPath) -> Path:
        """
        Extracts the tail difference between a root path and one of its sub-paths
        :param path: sub-path to consider
        :return: tail difference path
        """

        if self.root_path not in Path(path).parents:
            raise ValueError(f"Provided file path must be within {self.root_path}")

        directory_path = Path(path).parent.resolve()

        common_path_str = os.path.commonpath([self.root_path, directory_path])
        common_path_obj = Path(common_path_str)
        common_path_len = len(common_path_obj.parts)

        path_diff_parts = directory_path.parts[common_path_len:]
        return Path(*path_diff_parts)

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
