# restore_tool.py

import os
from backup.backup_manager import list_backup_sessions, restore_file_from_session
from utils.logger import get_logger

logger = get_logger(__name__)


def show_sessions():
    sessions = list_backup_sessions()
    if not sessions:
        logger.info("Keine Backup-Sessions gefunden.")
        return []

    logger.info("\n=== AutoNest Backup-Sessions ===")
    for i, s in enumerate(sessions):
        logger.info("[%s] %s", i, s)
    return sessions


def choose_session(sessions):
    index = input("Welche Session wiederherstellen? [Nummer]: ").strip()
    if not index.isdigit() or int(index) >= len(sessions):
        logger.warning("Ungültige Auswahl.")
        return None
    return sessions[int(index)]


def list_files_in_session(session_dir):
    path = os.path.join(".autonest_backups", session_dir)
    return os.listdir(path)


def choose_file(files):
    logger.info("\nDateien in der Session:")
    for i, f in enumerate(files):
        logger.info("[%s] %s", i, f)
    index = input("Welche Datei wiederherstellen? [Nummer]: ").strip()
    if not index.isdigit() or int(index) >= len(files):
        logger.warning("Ungültige Auswahl.")
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
    logger.info("\n=== Wiederhergestellt ===")
    logger.info(result)


def main() -> None:
    """Entry point for the restore tool."""
    restore_workflow()


if __name__ == "__main__":
    main()
