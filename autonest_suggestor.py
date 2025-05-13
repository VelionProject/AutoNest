# autonest_suggestor.py

import ast
from insertion_finder import find_best_insertion_point

def extract_metadata(code_str):
    """
    Extrahiert Metadaten wie Funktionsname, Argumente etc.
    """
    try:
        node = ast.parse(code_str)
        for element in node.body:
            if isinstance(element, ast.FunctionDef):
                name = element.name
                args = [arg.arg for arg in element.args.args]
                return {
                    "typ": "funktion",
                    "name": name,
                    "argumente": args,
                    "zeilen": len(code_str.strip().splitlines())
                }
            elif isinstance(element, ast.ClassDef):
                return {
                    "typ": "klasse",
                    "name": element.name,
                    "zeilen": len(code_str.strip().splitlines())
                }
        return {"typ": "unbekannt", "info": "Kein Funktions- oder Klassenkopf erkannt"}
    except SyntaxError:
        return {"typ": "fehler", "info": "Syntaxfehler"}

def suggest_insertion(code_str, project_path):
    """
    Gibt eine strukturierte Empfehlung, ob Code neu eingefügt oder erweitert werden sollte.
    """
    metadata = extract_metadata(code_str)
    matches = find_best_insertion_point(code_str, project_path)

    if not matches:
        return {
            "vermuteter_modus": "neu",
            "begründung": "Keine relevante Ähnlichkeit im Projekt erkannt.",
            "sicherheit": "mittel",
            "metadaten": metadata
        }

    best = matches[0]
    score = best["score"]
    modus = "erweitern" if score > 0.75 else "neu"

    return {
        "vermuteter_modus": modus,
        "ziel_datei": best["file"],
        "ziel_funktion": best["match_in_project"],
        "begründung": f"Ähnlichkeit zu bestehender Funktion: {int(score*100)}%",
        "sicherheit": "hoch" if score > 0.85 else "mittel",
        "metadaten": metadata
    }

# Beispieltest
if __name__ == "__main__":
    test_code = """
def validate_file_size(path):
    return os.path.getsize(path) > 10000000
"""
    pfad = input("Projektpfad: ").strip()
    from pprint import pprint
    pprint(suggest_insertion(test_code, pfad))
