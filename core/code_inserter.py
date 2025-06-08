# code_inserter.py

import ast
import os
import tempfile
import textwrap

from core.insertion_finder import (
    find_best_insertion_point,
    NoFunctionFoundError,
)
from backup.backup_manager import create_backup_session, backup_file_to_session


def insert_code_into_file(code_str, project_path, modus="neu"):
    """Insert code into a project file determined by ``find_best_insertion_point``.

    The function now uses :mod:`ast` to reliably locate the target function and
    compute the correct insertion position. This preserves indentation and also
    works with decorated or nested functions.
    """

    try:
        match_list = find_best_insertion_point(code_str, project_path)
    except NoFunctionFoundError as exc:
        return {"error": str(exc)}

    if not match_list:
        return {"error": "Kein geeigneter Einfügepunkt gefunden"}

    best = match_list[0]
    target_file = best["file"]
    insert_target = best["match_in_project"]

    try:
        with open(target_file, "r", encoding="utf-8") as fh:
            source = fh.read()
        tree = ast.parse(source)
    except SyntaxError as exc:
        return {"error": f"Fehler beim Parsen der Zieldatei: {exc}"}

    lines = source.splitlines(keepends=True)
    snippet = textwrap.dedent(code_str).splitlines(keepends=True)
    if snippet and not snippet[-1].endswith("\n"):
        snippet[-1] += "\n"

    func_node = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == insert_target:
            func_node = node
            break

    if func_node is None or func_node.end_lineno is None:
        return {"error": "Einfügestelle konnte nicht lokalisiert werden"}

    if modus == "erweitern":
        indent = " " * (func_node.col_offset + 4)
        insert_at = func_node.end_lineno
        extended = [indent + l.lstrip() if l.strip() else l for l in snippet]
        lines[insert_at:insert_at] = extended
    else:
        indent = " " * func_node.col_offset
        insert_at = func_node.end_lineno
        new_block = [indent + line if line.strip() else line for line in snippet]
        lines[insert_at:insert_at] = ["\n"] + new_block + ["\n"]

    updated_source = "".join(lines)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8")
    temp.write(updated_source)
    temp.close()

    try:
        with open(temp.name, "r", encoding="utf-8") as fh:
            ast.parse(fh.read())
    except SyntaxError as exc:
        os.unlink(temp.name)
        return {"error": f"Fehler beim Kompilieren: {exc}"}

    with open(target_file, "w", encoding="utf-8") as fh:
        fh.write(updated_source)

    os.unlink(temp.name)
    return {
        "status": "Code eingefügt",
        "datei": target_file,
        "modus": modus,
        "ziel": insert_target,
    }


def safe_insert_code(code_str, project_path, modus="neu"):
    """
    Kombiniert Backup + Code-Einfügung automatisch.
    """
    try:
        match_list = find_best_insertion_point(code_str, project_path)
    except NoFunctionFoundError as exc:
        return {"error": str(exc)}
    if not match_list:
        return {"error": "Kein Einfügepunkt gefunden"}

    best = match_list[0]
    target_file = best["file"]

    # Backup-Ordner erstellen und Datei sichern
    session_dir = create_backup_session()
    backup_file_to_session(target_file, session_dir)

    result = insert_code_into_file(code_str, project_path, modus=modus)
    result["backup_session"] = session_dir
    return result


# Beispiel zum Testen
if __name__ == "__main__":
    test_code = """
def calculate_checksum(data):
    return sum(data)
"""
    pfad = input("Projektpfad: ").strip()
    res = safe_insert_code(test_code, pfad, modus="neu")
    from pprint import pprint

    pprint(res)
