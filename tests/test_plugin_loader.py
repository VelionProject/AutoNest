import sys
import os

sys.path.insert(0, os.getcwd())
from plugins import load_plugins


def test_sample_plugin_loaded():
    rules = load_plugins()
    assert any(callable(r) for r in rules)
