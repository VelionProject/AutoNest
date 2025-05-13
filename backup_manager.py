# backup_manager.py

import os
import shutil
from datetime import datetime

ROOT_BACKUP_DIR = ".autonest_backups"

def create_backup_session():
    """
    Erstellt einen neuen Unterordner für die aktuelle Backup-Session.
    Gibt den Pfad zurück.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_dir = os.path.join(ROOT_BACKUP_DIR, timestamp)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir

def backup_file_to_session(file_path, session_dir):
    """
    Kopiert eine einzelne Datei in das angegebene Session-Verzeichnis.
    """
    filename = os.path.basename(file_path)
    dest_path = os.path.join(session_dir, filename)
    shutil.copy(file_path, dest_path)
    return dest_path

def list_backup_sessions():
    """
    Gibt alle Session-Ordner im .autonest_backups-Verzeichnis zurück.
    """
    if not os.path.exists(ROOT_BACKUP_DIR):
        return []
    return sorted(os.listdir(ROOT_BACKUP_DIR), reverse=True)

def restore_file_from_session(session_name, filename, project_path="."):
    """
    Stellt eine bestimmte Datei aus einer bestimmten Session wieder her.
    """
    session_path = os.path.join(ROOT_BACKUP_DIR, session_name)
    if not os.path.exists(session_path):
        return f"Session {session_name} nicht gefunden."

    backup_file = os.path.join(session_path, filename)
    if not os.path.exists(backup_file):
        return f"{filename} nicht in {session_name} gefunden."

    target_path = os.path.join(project_path, filename)
    shutil.copy(backup_file, target_path)
    return f"{filename} wurde aus {session_name} wiederhergestellt."

# Beispielnutzung
if __name__ == "__main__":
    print("Verfügbare Sessions:")
    for s in list_backup_sessions():
        print(" -", s)
