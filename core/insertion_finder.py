# insertion_finder.py

import ast
from difflib import SequenceMatcher
from core.project_scanner import scan_project_structure

def extract_function_names(code_str):
    """
    Holt Funktionsnamen aus einem Code-String (z. B. einem neuen Block).
    """
    try:
        node = ast.parse(code_str)
        return [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
    except SyntaxError:
        return []

def similarity(a, b):
    """
    Einfacher Ähnlichkeitswert zwischen zwei Strings (z. B. Funktionsnamen).
    """
    return SequenceMatcher(None, a, b).ratio()

def find_best_insertion_point(code_str, project_path):
    """
    Vergleicht den eingegebenen Code mit allen Funktionen im Projekt.
    Gibt die am besten passende Datei zurück.
    """
    target_names = extract_function_names(code_str)
    if not target_names:
        return {"error": "Keine gültige Funktion erkannt"}

    structure = scan_project_structure(project_path)
    matches = []

    for module in structure:
        for func in module.get("functions", []):
            for target in target_names:
                score = similarity(target, func)
                if score > 0.5:  # Schwelle einstellbar
                    matches.append({
                        "target": target,
                        "match_in_project": func,
                        "file": module["file"],
                        "score": round(score, 3)
                    })

    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:5]  # Top 5 Matches zurückgeben

# Beispieltest
if __name__ == "__main__":
    from pprint import pprint
    test_code = """
def calculate_checksum(data):
    return sum(data)
"""
    pfad = input("Projektpfad eingeben: ").strip()
    pprint(find_best_insertion_point(test_code, pfad))
