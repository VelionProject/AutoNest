# autonest_semantics.py

"""Logic for choosing between GPT and local suggestion."""

import os
from utils.config import load_config

cfg = load_config()
env_value = os.getenv("AUTONEST_USE_GPT")
if env_value is not None:
    USE_GPT = env_value.lower() in ("1", "true", "yes")
else:
    USE_GPT = cfg.get("use_gpt", False)

if USE_GPT:
    from core.autonest_gpt import suggest_with_gpt as suggest_logic
    from core.project_scanner import scan_project_structure
else:
    from core.autonest_suggestor import suggest_insertion as suggest_logic


def suggest(code_str, project_path):
    if USE_GPT:
        structure = scan_project_structure(project_path)
        return suggest_logic(code_str, structure)
    else:
        return suggest_logic(code_str, project_path)
