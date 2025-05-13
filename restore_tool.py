# restore_tool.py

import os
from backup_manager import list_backup_sessions, restore_file_from_session

def show_sessions():
    sessions = list_backup_sessions()
    if not sessions:
        print("Keine Backup-Sessions gefunden.")
        return []

    print("\n=== AutoNest Backup-Sessions ===")
    for i, s in enumerate(sessions):
        print(f"[{i}] {s}")
    return sessions

def choose_session(sessions):
    index = input("Welche Session wiederherstellen? [Nummer]: ").strip()
    if not index.isdigit() or int(index) >= len(sessions):
        print("Ungültige Auswahl.")
        return None
    return sessions[int(index)]

def list_files_in_session(session_dir):
    path = os.path.join(".autonest_backups", session_dir)
    return os.listdir(path)

def choose_file(files):
    print("\nDateien in der Session:")
    for i, f in enumerate(files):
        print(f"[{i}] {f}")
    index = input("Welche Datei wiederherstellen? [Nummer]: ").strip()
    if not index.isdigit() or int(index) >= len(files):
        print("Ungültige Auswahl.")
        return None
    return files[int(index)]

def restore_workflow():
    sessions = show_sessions()
    if not sessions:
        return
    session = choose_session(sessions)
    if not session:
        return
    files = list_files_in_session(session)
    file = choose_file(files)
    if not file:
        return
    result = restore_file_from_session(session, file)
    print("\n=== Wiederhergestellt ===")
    print(result)

if __name__ == "__main__":
    restore_workflow()
