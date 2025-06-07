import importlib
import pkgutil
import os


def load_plugins():
    plugins = []
    base = os.path.dirname(__file__)
    for _, name, _ in pkgutil.iter_modules([base]):
        module = importlib.import_module(f"{__package__}.{name}")
        if hasattr(module, "get_rules"):
            plugins.extend(module.get_rules())
    return plugins
