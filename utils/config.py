import json
import os

DEFAULT_CONFIG = {"backup_dir": ".autonest_backups", "use_gpt": False, "default_project_path": ""}


def load_config(path="config.json"):
    if not os.path.exists(path):
        return DEFAULT_CONFIG.copy()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cfg = DEFAULT_CONFIG.copy()
    cfg.update(data)
    return cfg


def save_config(config, path="config.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
