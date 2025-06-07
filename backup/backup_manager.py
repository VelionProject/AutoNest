# backup_manager.py

import os
import shutil
from datetime import datetime
from utils.logger import get_logger
from utils.config import load_config

config = load_config()
ROOT_BACKUP_DIR = config.get("backup_dir", ".autonest_backups")
logger = get_logger(__name__)


def create_backup_session():
    """
    Erstellt einen neuen Unterordner für die aktuelle Backup-Session.
    Gibt den Pfad zurück.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_dir = os.path.join(ROOT_BACKUP_DIR, timestamp)
    try:
        os.makedirs(session_dir, exist_ok=True)
    except OSError as exc:
        logger.error("Kann Backup-Ordner nicht erstellen: %s", exc)
        raise
    return session_dir


def backup_file_to_session(file_path, session_dir):
    """
    Kopiert eine einzelne Datei in das angegebene Session-Verzeichnis.
    """
    filename = os.path.basename(file_path)
    dest_path = os.path.join(session_dir, filename)
    try:
        shutil.copy(file_path, dest_path)
    except (OSError, shutil.Error) as exc:
        logger.error("Fehler beim Kopieren %s: %s", file_path, exc)
        raise
    return dest_path


def list_backup_sessions():
    """
    Gibt alle Session-Ordner im .autonest_backups-Verzeichnis zurück.
    """
    if not os.path.exists(ROOT_BACKUP_DIR):
        return []
    try:
        return sorted(os.listdir(ROOT_BACKUP_DIR), reverse=True)
    except OSError as exc:
        logger.error("Fehler beim Lesen der Backup-Sessions: %s", exc)
        return []


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
    try:
        shutil.copy(backup_file, target_path)
    except (OSError, shutil.Error) as exc:
        logger.error("Fehler beim Wiederherstellen %s: %s", filename, exc)
        return f"Fehler beim Wiederherstellen von {filename}."
    return f"{filename} wurde aus {session_name} wiederhergestellt."


# Beispielnutzung
if __name__ == "__main__":
    logger.info("Verfügbare Sessions:")
    for s in list_backup_sessions():
        logger.info(" - %s", s)
