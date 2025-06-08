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
    from core.autonest_suggestor import suggest_insertion as suggest_logic
    from core.autonest_gpt import describe_project_with_gpt
else:
    from core.autonest_suggestor import suggest_insertion as suggest_logic


def suggest(code_str, project_path):
    if USE_GPT:
        project_summary = describe_project_with_gpt(project_path)
        return suggest_logic(code_str, project_summary=project_summary)
    else:
        return suggest_logic(code_str, project_path=project_path)
