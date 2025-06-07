import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath("core"))
from project_scanner import scan_python_files, extract_structure


def test_scan_python_files_and_structure():
    with tempfile.TemporaryDirectory() as tmp:
        file1 = os.path.join(tmp, "a.py")
        with open(file1, "w", encoding="utf-8") as f:
            f.write("""\nclass A:\n    pass\n\ndef func():\n    pass\n""")
        files = scan_python_files(tmp)
        assert file1 in files
        structure = extract_structure(file1)
        assert "A" in structure["classes"]
        assert "func" in structure["functions"]
