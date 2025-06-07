# code_inserter.py

import ast
import os
import tempfile

from core.insertion_finder import find_best_insertion_point
from backup.backup_manager import create_backup_session, backup_file_to_session


def insert_code_into_file(code_str, project_path, modus="neu"):
    """
    Führt die eigentliche Code-Einfügung durch (ohne Backup).
    """
    match_list = find_best_insertion_point(code_str, project_path)
    if not match_list:
        return {"error": "Kein geeigneter Einfügepunkt gefunden"}

    best = match_list[0]
    target_file = best["file"]
    insert_target = best["match_in_project"]

    with open(target_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_code_lines = code_str.strip().splitlines(keepends=True)

    if modus == "erweitern":
        inside_target = False
        indent_level = None
        insert_index = None

        for i, line in enumerate(lines):
            if f"def {insert_target}" in line:
                inside_target = True
                indent_level = len(line) - len(line.lstrip())
                continue
            if inside_target:
                if len(line.strip()) == 0:
                    continue
                curr_indent = len(line) - len(line.lstrip())
                if curr_indent <= indent_level:
                    insert_index = i
                    break

        if insert_index is None:
            insert_index = len(lines)

        body_indent = " " * (indent_level + 4)
        extended_body = [body_indent + l.lstrip() for l in new_code_lines]

        updated = lines[:insert_index] + extended_body + ["\n"] + lines[insert_index:]

    else:
        insert_index = None
        for idx, line in enumerate(lines):
            if f"def {insert_target}" in line:
                insert_index = idx
                break

        if insert_index is None:
            return {"error": "Einfügestelle konnte nicht lokalisiert werden"}

        end_index = insert_index
        indent_level = len(lines[insert_index]) - len(lines[insert_index].lstrip())

        for i in range(insert_index + 1, len(lines)):
            if len(lines[i].strip()) == 0:
                continue
            curr_indent = len(lines[i]) - len(lines[i].lstrip())
            if curr_indent <= indent_level:
                end_index = i
                break

        updated = lines[:end_index] + ["\n"] + new_code_lines + ["\n"] + lines[end_index:]

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8")
    temp.writelines(updated)
    temp.close()

    try:
        with open(temp.name, "r", encoding="utf-8") as f:
            ast.parse(f.read())
    except SyntaxError as e:
        os.unlink(temp.name)
        return {"error": f"Fehler beim Kompilieren: {e}"}

    with open(target_file, "w", encoding="utf-8") as f:
        f.writelines(updated)

    os.unlink(temp.name)
    return {"status": "Code eingefügt", "datei": target_file, "modus": modus, "ziel": insert_target}


def safe_insert_code(code_str, project_path, modus="neu"):
    """
    Kombiniert Backup + Code-Einfügung automatisch.
    """
    match_list = find_best_insertion_point(code_str, project_path)
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
