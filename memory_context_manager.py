import os
import json
from datetime import datetime

MEMORY_FILENAME = ".autonest_memory.jsonl"


def get_memory_path(project_path):
    return os.path.join(project_path, MEMORY_FILENAME)


def save_context_entry(project_path, suggestion, code, user_override=False):
    memory_path = get_memory_path(project_path)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "file_target": suggestion.get("ziel_datei"),
        "function_target": suggestion.get("ziel_funktion"),
        "mode": suggestion.get("vermuteter_modus"),
        "decision_safety": suggestion.get("sicherheit"),
        "raw_code": code.strip(),
        "user_override": user_override
    }
    with open(memory_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def load_recent_entries(project_path, limit=5):
    memory_path = get_memory_path(project_path)
    if not os.path.exists(memory_path):
        return []
    with open(memory_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    entries = [json.loads(line) for line in lines[-limit:]]
    return entries


def clear_memory(project_path):
    memory_path = get_memory_path(project_path)
    if os.path.exists(memory_path):
        os.remove(memory_path)
