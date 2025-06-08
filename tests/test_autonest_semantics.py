import os
import sys
import importlib
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_suggest_describes_project_once(monkeypatch):
    fake_openai = types.SimpleNamespace(
        ChatCompletion=types.SimpleNamespace(
            create=lambda *a, **k: {"choices": [{"message": {"content": ""}}]}
        )
    )
    monkeypatch.setitem(sys.modules, "openai", fake_openai)

    os.environ["AUTONEST_USE_GPT"] = "1"
    import core.autonest_semantics as semantics

    importlib.reload(semantics)

    calls = []

    def fake_desc(path):
        calls.append(path)
        return "summary"

    monkeypatch.setattr(semantics, "describe_project_with_gpt", fake_desc)

    captured = {}

    def fake_logic(code_str, project_summary=None, project_path=None):
        captured["summary"] = project_summary
        captured["path"] = project_path
        return {}

    monkeypatch.setattr(semantics, "suggest_logic", fake_logic)

    semantics.suggest("code", "/tmp/proj")

    assert calls == ["/tmp/proj"]
    assert captured["summary"] == "summary"
    assert captured["path"] is None
