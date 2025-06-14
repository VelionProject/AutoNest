import importlib
import pkgutil
import os
from utils.config import load_config, save_config
from utils.logger import get_logger

logger = get_logger(__name__)


def list_plugins():
    """Return all available plugin module names."""
    base = os.path.dirname(__file__)
    return [name for _, name, _ in pkgutil.iter_modules([base]) if not name.startswith("_")]


def set_plugin_status(name, active=True):
    """Persist activation status for a plugin."""
    cfg = load_config()
    modules = cfg.setdefault("modules", {})
    modules[name] = bool(active)
    save_config(cfg)


def load_plugins():
    cfg = load_config()
    active = cfg.get("modules", {})
    plugins = []
    base = os.path.dirname(__file__)
    for _, name, _ in pkgutil.iter_modules([base]):
        if name.startswith("_"):
            continue
        if name in active and not active[name]:
            continue
        try:
            module = importlib.import_module(f"{__package__}.{name}")
        except ImportError as exc:
            logger.warning("Plugin '%s' konnte nicht geladen werden: %s", name, str(exc))
            continue
        if hasattr(module, "get_rules"):
            try:
                plugins.extend(module.get_rules())
            except Exception as exc:  # noqa: BLE001
                logger.warning("Plugin '%s' konnte nicht initialisiert werden: %s", name, str(exc))
    return plugins
