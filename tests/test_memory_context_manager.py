import os
import tempfile
from backup import memory_context_manager as mcm


def test_save_and_load_recent_entries():
    with tempfile.TemporaryDirectory() as tmp:
        suggestion = {
            "ziel_datei": "foo.py",
            "ziel_funktion": "bar",
            "vermuteter_modus": "neu",
            "sicherheit": "hoch",
        }
        # clear to start
        mcm.clear_memory(tmp)
        for i in range(7):
            mcm.save_context_entry(tmp, suggestion, f"print({i})")
        entries = mcm.load_recent_entries(tmp)
        assert len(entries) == 5
        assert entries[-1]["raw_code"] == "print(6)"
        # limit 2
        entries2 = mcm.load_recent_entries(tmp, limit=2)
        assert len(entries2) == 2
        assert entries2[0]["raw_code"] == "print(5)"
