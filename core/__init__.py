"""Core functionality for AutoNest."""

from .code_inserter import insert_code_into_file, safe_insert_code
from .insertion_finder import find_best_insertion_point, NoFunctionFoundError
from .project_scanner import scan_project_structure, describe_project_locally

__all__ = [
    "insert_code_into_file",
    "safe_insert_code",
    "find_best_insertion_point",
    "NoFunctionFoundError",
    "scan_project_structure",
    "describe_project_locally",
    "suggest",
]


def suggest(code_str, project_path):
    """Proxy to :func:`autonest_semantics.suggest` with lazy import."""
    from .autonest_semantics import suggest as _suggest

    return _suggest(code_str, project_path)
