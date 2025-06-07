import tempfile
import os
import sys

# Add project root to PYTHONPATH so tests work when executed from the
# tests directory or via CI tools where the working directory may not be
# the repository root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.insertion_finder import find_best_insertion_point


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
