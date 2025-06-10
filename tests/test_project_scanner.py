import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.project_scanner import (
    scan_python_files,
    extract_structure,
    describe_project_locally,
)


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


def test_describe_project_locally_imports():
    with tempfile.TemporaryDirectory() as tmp:
        file1 = os.path.join(tmp, "mod.py")
        with open(file1, "w", encoding="utf-8") as f:
            f.write(
                (
                    "import os\n"
                    "from pkg import mod as m\n\n"
                    "class B:\n    pass\n\n"
                    "def func():\n    pass\n"
                )
            )

        result = describe_project_locally(tmp)
        assert "Funktionen: 1" in result
        assert "Klassen: 1" in result
        assert "os" in result
        assert "pkg.mod" in result
