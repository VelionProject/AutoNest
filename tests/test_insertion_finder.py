import tempfile
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.insertion_finder import find_best_insertion_point, NoFunctionFoundError


def test_find_best_insertion_point():
    with tempfile.TemporaryDirectory() as tmp:
        os.mkdir(os.path.join(tmp, "sub"))
        file1 = os.path.join(tmp, "sub", "module.py")
        with open(file1, "w", encoding="utf-8") as f:
            f.write("""\ndef existing_func():\n    pass\n""")
        code = """\ndef existing_func():\n    print('hi')\n"""
        matches = find_best_insertion_point(code, tmp)
        assert matches
        assert matches[0]["file"] == file1


def test_no_function_found_error():
    with tempfile.TemporaryDirectory() as tmp:
        code = "print('no func')"
        with pytest.raises(NoFunctionFoundError):
            find_best_insertion_point(code, tmp)
