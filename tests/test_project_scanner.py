import tempfile
import os
import sys

# Add project root to PYTHONPATH so tests work when executed from the
# tests directory or via CI tools where the working directory may not be
# the repository root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.project_scanner import scan_python_files, extract_structure


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
