# autonest_cli.py

from core.code_inserter import insert_code_into_file
from core.insertion_finder import (
    find_best_insertion_point,
    NoFunctionFoundError,
)
from pprint import pprint
import os
from utils.logger import get_logger

logger = get_logger(__name__)


def decide_mode_and_confirm(code_str, project_path):
    try:
        matches = find_best_insertion_point(code_str, project_path)
    except NoFunctionFoundError as exc:
        logger.warning(str(exc))
        return
    if not matches:
        logger.warning("Kein passender Ort im Projekt gefunden.")
        return

    best = matches[0]
    file = best["file"]
    func = best["match_in_project"]
    score = best["score"]

    # Entscheidung: Erweiterung oder neue Funktion?
    modus = "erweitern" if score > 0.75 else "neu"

    logger.info("\n=== Vorschlag von AutoNest ===")
    logger.info("Modus       : %s", modus.upper())
    logger.info("Zieldatei   : %s", file)
    logger.info("Zielobjekt  : %s", func)
    logger.info("Ähnlichkeit : %s %%", int(score * 100))

    confirm = input("\nWillst du das so ausführen? [J/N]: ").strip().lower()
    if confirm == "j":
        result = insert_code_into_file(code_str, project_path, modus=modus)
        logger.info("\n--- Ergebnis ---")
        logger.info(result)
    else:
        logger.info("Abgebrochen.")


def main() -> None:
    """Command-line interface entry point."""
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


if __name__ == "__main__":
    main()
