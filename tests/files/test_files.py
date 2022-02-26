# -*- coding: utf-8 -*-

import tempfile
import shutil

from pathlib import Path
from typing import Generator
from typing import List
from typing import Tuple

import pytest

from src.job.files import FileSystemIterator


TEST_EXTENSION = ".test"


@pytest.fixture(scope="function")
def tmp_files(tmp_path: Path) -> Generator:
    """
    Fixture to make a list of temporal files available during the duration of a test
    :param tmp_path: Pytest provided fixture to use as base path
    :return: tuple of temp directory and list of temp file paths
    """

    tmp_dir = tmp_path

    tmp_files = [
        tempfile.mkstemp(suffix=TEST_EXTENSION, dir=tmp_dir),
        tempfile.mkstemp(suffix=TEST_EXTENSION, dir=tmp_dir),
        tempfile.mkstemp(suffix=TEST_EXTENSION, dir=tmp_dir),
    ]

    tmp_file_paths = [tmp_file[1] for tmp_file in tmp_files]

    try:
        yield tmp_dir, tmp_file_paths
    finally:
        shutil.rmtree(tmp_dir)


def test_file_iterator_get_diff(tmp_path: Path):
    """
    Tests the correct sub-path diff logic of the FileSystemIterator class
    :param tmp_path: Pytest provided fixture to use as base path
    """

    tmp_dir = tmp_path / "A" / "B" / "C"
    tmp_dir.mkdir(parents=True)

    iterator = FileSystemIterator(tmp_dir, ".test")

    assert iterator.get_path_diff(tmp_dir / "file.test") == Path(".")
    assert iterator.get_path_diff(tmp_dir / "D" / "file.test") == Path("D")

    assert pytest.raises(ValueError, iterator.get_path_diff, tmp_dir)
    assert pytest.raises(ValueError, iterator.get_path_diff, tmp_path / "A")
    assert pytest.raises(ValueError, iterator.get_path_diff, tmp_path / "E")


def test_file_iterator_all_paths(tmp_files: Tuple[str, List[str]]):
    """
    Tests the correct listing of files sub-paths by the FileSystemIterator class
    :param tmp_files: tuple of tmp directory and list of tmp file paths
    """

    (tmp_dir, tmp_file_paths) = tmp_files

    iterator = FileSystemIterator(tmp_dir, TEST_EXTENSION)
    file_paths = iterator.all_paths()

    assert len(file_paths) == len(tmp_file_paths)
    assert all(Path(path).is_file() for path in file_paths)
    assert all(Path(path).suffix == TEST_EXTENSION for path in file_paths)
