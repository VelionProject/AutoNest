import tempfile
import os
import sys

# Add project root to PYTHONPATH so tests work when executed from the
# tests directory or via CI tools where the working directory may not be
# the repository root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backup import backup_manager


def test_backup_and_restore():
    with tempfile.TemporaryDirectory() as tmp:
        file_path = os.path.join(tmp, "file.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("data")
        backup_manager.ROOT_BACKUP_DIR = os.path.join(tmp, "backups")
        session = backup_manager.create_backup_session()
        backup_manager.backup_file_to_session(file_path, session)
        filename = os.path.basename(file_path)
        # restore to new folder
        restore_target = os.path.join(tmp, "restore")
        os.makedirs(restore_target)
        result = backup_manager.restore_file_from_session(
            os.path.basename(session), filename, restore_target
        )
        assert "wiederhergestellt" in result.lower()
        assert os.path.exists(os.path.join(restore_target, filename))
