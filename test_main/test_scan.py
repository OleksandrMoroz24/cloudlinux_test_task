import os
import pytest
from main import scan_directory


@pytest.fixture
def create_files(tmp_path):
    (tmp_path / "dir").mkdir()
    (tmp_path / "dir" / "file.txt").write_text("content")
    (tmp_path / "dir" / "large_file.txt").write_text("content" * 10000)
    return tmp_path / "dir"


def test_scan_directory_with_size_threshold(capsys, create_files):
    scan_directory(str(create_files), size_threshold=1024, prefix="")
    captured = capsys.readouterr()
    assert "large_file.txt" in captured.out
    assert "file.txt" in captured.out


def test_scan_directory_output(capsys, create_files):
    scan_directory(str(create_files), size_threshold=0, prefix="")
    captured = capsys.readouterr()
    assert "file.txt" in captured.out
    assert "large_file.txt" in captured.out
    assert "Total size of files:" in captured.out
