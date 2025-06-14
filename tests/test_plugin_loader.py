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


def test_faulty_plugin_is_skipped(monkeypatch):
    plugin_dir = os.path.join(os.path.dirname(__file__), "..", "plugins")
    faulty_path = os.path.join(plugin_dir, "faulty_plugin.py")
    with open(faulty_path, "w", encoding="utf-8") as fh:
        fh.write('raise ImportError("boom")')

    warnings = []
    from plugins import plugin_loader

    monkeypatch.setattr(
        plugin_loader.logger, "warning", lambda *args, **kwargs: warnings.append(args)
    )
    try:
        rules = plugin_loader.load_plugins()
        assert any(callable(r) for r in rules)
        assert warnings
    finally:
        os.remove(faulty_path)


def test_rules_exception_is_skipped(monkeypatch):
    plugin_dir = os.path.join(os.path.dirname(__file__), "..", "plugins")
    bad_path = os.path.join(plugin_dir, "bad_rules_plugin.py")
    with open(bad_path, "w", encoding="utf-8") as fh:
        fh.write("def get_rules():\n    raise RuntimeError('fail')\n")

    warnings = []
    from plugins import plugin_loader

    monkeypatch.setattr(
        plugin_loader.logger, "warning", lambda *args, **kwargs: warnings.append(args)
    )
    try:
        rules = plugin_loader.load_plugins()
        assert any(callable(r) for r in rules)
        assert warnings
    finally:
        os.remove(bad_path)
