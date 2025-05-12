# autonest_semantics.py

# Schalter: True = GPT verwenden, False = lokalen Suggestor
USE_GPT = False  # ← Ändere das später auf True, wenn du GPT willst

if USE_GPT:
    from autonest_gpt import suggest_with_gpt as suggest_logic
    from project_scanner import scan_project_structure
else:
    from autonest_suggestor import suggest_insertion as suggest_logic

def suggest(code_str, project_path):
    if USE_GPT:
        structure = scan_project_structure(project_path)
        return suggest_logic(code_str, structure)
    else:
        return suggest_logic(code_str, project_path)
