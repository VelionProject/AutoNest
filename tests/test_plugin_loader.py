import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from plugins import load_plugins


def test_sample_plugin_loaded():
    rules = load_plugins()
    assert any(callable(r) for r in rules)


def test_plugin_can_be_disabled(tmp_path, monkeypatch):
    cfg = {"modules": {"sample_plugin": False}}
    cfg_path = tmp_path / "config.json"
    with open(cfg_path, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh)
    monkeypatch.chdir(tmp_path)
    rules = load_plugins()
    assert not rules
