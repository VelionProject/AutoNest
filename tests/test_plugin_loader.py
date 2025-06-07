import sys
import os

# Add project root to PYTHONPATH so tests work when executed from the
# tests directory or via CI tools where the working directory may not be
# the repository root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from plugins import load_plugins


def test_sample_plugin_loaded():
    rules = load_plugins()
    assert any(callable(r) for r in rules)
