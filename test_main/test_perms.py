import os
import pytest
from main import analyze_permissions



@pytest.fixture
def setup_files_with_permissions(tmp_path):
    # Створення файлу з "звичайними" дозволами
    normal_file = tmp_path / "normal_file.txt"
    normal_file.touch()
    normal_file.chmod(0o644)

    # Створення файлу з "незвичайними" дозволами
    unusual_file = tmp_path / "unusual_file.txt"
    unusual_file.touch()
    unusual_file.chmod(
        0o777
    )  # Встановлення дозволів на читання, запис та виконання для всіх

    return tmp_path


def test_analyze_permissions(capsys, setup_files_with_permissions):
    analyze_permissions(str(setup_files_with_permissions))
    captured = capsys.readouterr()

    # Перевірка, що файл з незвичайними дозволами був знайдений
    assert "unusual_file.txt: Permissions 777" in captured.out

    # Перевірка, що файл зі звичайними дозволами не був знайдений як незвичайний
    assert "normal_file.txt" not in captured.out
