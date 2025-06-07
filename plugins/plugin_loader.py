import importlib
import pkgutil
import os
from utils.config import load_config, save_config


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
        module = importlib.import_module(f"{__package__}.{name}")
        if hasattr(module, "get_rules"):
            plugins.extend(module.get_rules())
    return plugins
