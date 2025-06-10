# project_scanner.py

import os
import ast


def scan_python_files(project_path):
    """
    Durchsucht alle Unterordner eines Projekts nach .py-Dateien.
    Gibt eine Liste von Dateipfaden zurück.
    """
    python_files = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def extract_structure(file_path):
    """
    Öffnet eine Python-Datei, analysiert sie mit ast,
    und extrahiert alle Klassen- und Funktionsnamen.
    Gibt ein Dictionary mit Struktur zurück.
    """
    structure = {"file": file_path, "classes": [], "functions": []}

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            node = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            structure["error"] = "Syntaxfehler beim Parsen"
            return structure

    for element in node.body:
        if isinstance(element, ast.ClassDef):
            structure["classes"].append(element.name)
        elif isinstance(element, ast.FunctionDef):
            structure["functions"].append(element.name)

    return structure


def scan_project_structure(project_path):
    """
    Hauptfunktion: scannt das Projekt und erstellt
    eine Übersicht über alle Python-Dateien inkl. deren Struktur.
    """
    project_map = []
    files = scan_python_files(project_path)
    for file_path in files:
        structure = extract_structure(file_path)
        project_map.append(structure)
    return project_map


def describe_project_locally(project_path):
    import os
    import ast

    function_count = 0
    class_count = 0
    modules = set()

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                with open(full_path, encoding="utf-8") as f:
                    source = f.read()

                lines = source.splitlines()
                for line in lines:
                    if line.strip().startswith("def "):
                        function_count += 1
                    elif line.strip().startswith("class "):
                        class_count += 1

                try:
                    tree = ast.parse(source, filename=full_path)
                except SyntaxError:
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            modules.add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        module_base = node.module or ""
                        for alias in node.names:
                            if module_base:
                                modules.add(f"{module_base}.{alias.name}")
                            else:
                                modules.add(alias.name)

    return (
        f"Funktionen: {function_count}\nKlassen: {class_count}\nVerwendete "
        f"Module: {', '.join(sorted(modules))}"
    )


# Beispielnutzung (zum Testen):
if __name__ == "__main__":
    from pprint import pprint

    pfad = input("Pfad zum Projektordner eingeben: ").strip()
    pprint(scan_project_structure(pfad))
