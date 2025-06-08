import os
import sys
import tempfile
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core import code_inserter


def _fake_finder(file_path, func_name):
    def finder(code_str, project_path):
        return [{"file": str(file_path), "match_in_project": func_name, "score": 1.0}]

    return finder


def test_insert_into_decorated_function(tmp_path, monkeypatch):
    file_path = tmp_path / "mod.py"
    file_path.write_text("@dec\ndef target():\n    pass\n")

    monkeypatch.setattr(
        code_inserter, "find_best_insertion_point", _fake_finder(file_path, "target")
    )

    result = code_inserter.insert_code_into_file("print('x')", str(tmp_path), modus="erweitern")
    assert "error" not in result
    content = file_path.read_text().splitlines()
    assert "    print('x')" in content


def test_append_new_function_after_nested(tmp_path, monkeypatch):
    file_path = tmp_path / "pkg.py"
    file_path.write_text("class Foo:\n    def existing(self):\n        pass\n")

    monkeypatch.setattr(
        code_inserter, "find_best_insertion_point", _fake_finder(file_path, "existing")
    )

    new_func = "def new_func(self):\n    pass"
    result = code_inserter.insert_code_into_file(new_func, str(tmp_path), modus="neu")
    assert "error" not in result
    text = file_path.read_text().splitlines()
    assert any("def new_func" in line for line in text)
