# autonest_cli.py

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.code_inserter import insert_code_into_file
from core.insertion_finder import find_best_insertion_point
from pprint import pprint

def decide_mode_and_confirm(code_str, project_path):
    matches = find_best_insertion_point(code_str, project_path)
    if not matches:
        print("Kein passender Ort im Projekt gefunden.")
        return

    best = matches[0]
    file = best["file"]
    func = best["match_in_project"]
    score = best["score"]

    # Entscheidung: Erweiterung oder neue Funktion?
    modus = "erweitern" if score > 0.75 else "neu"

    print("\n=== Vorschlag von AutoNest ===")
    print(f"Modus       : {modus.upper()}")
    print(f"Zieldatei   : {file}")
    print(f"Zielobjekt  : {func}")
    print(f"Ähnlichkeit : {int(score * 100)} %")

    confirm = input("\nWillst du das so ausführen? [J/N]: ").strip().lower()
    if confirm == "j":
        result = insert_code_into_file(code_str, project_path, modus=modus)
        print("\n--- Ergebnis ---")
        pprint(result)
    else:
        print("Abgebrochen.")

# Beispielnutzung:
if __name__ == "__main__":
    pfad = input("Pfad zum Projekt: ").strip()
    print("Bitte füge deinen Code ein (Beende mit Leerzeile):")

    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    code = "\n".join(lines)
    decide_mode_and_confirm(code, pfad)
