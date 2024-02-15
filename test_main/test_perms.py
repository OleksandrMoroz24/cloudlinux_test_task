import os
import pytest
from main import analyze_permissions


@pytest.fixture
def setup_files_with_permissions(tmp_path):
    normal_file = tmp_path / "normal_file.txt"
    normal_file.touch()
    normal_file.chmod(0o644)

    unusual_file = tmp_path / "unusual_file.txt"
    unusual_file.touch()
    unusual_file.chmod(
        0o777
    )

    return tmp_path


def test_analyze_permissions(capsys, setup_files_with_permissions):
    analyze_permissions(str(setup_files_with_permissions))
    captured = capsys.readouterr()

    assert "unusual_file.txt: Permissions 777" in captured.out

    assert "normal_file.txt" not in captured.out
