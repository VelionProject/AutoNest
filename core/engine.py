"""High-level orchestration for AutoNest tasks.

This module provides :class:`AutoNestEngine`, a helper that coordinates
suggestion and insertion logic when working with a project.
"""

from __future__ import annotations

from .code_inserter import safe_insert_code


__all__ = ["AutoNestEngine"]


class AutoNestEngine:
    """Simple wrapper for performing AutoNest operations."""

    def __init__(self, project_path: str) -> None:
        """Create a new engine bound to ``project_path``."""

        self.project_path = project_path

    def suggest(self, code_str: str):
        """Return a suggestion about how to handle ``code_str``."""
        from . import autonest_semantics

        return autonest_semantics.suggest(code_str, self.project_path)

    def insert(self, code_str: str, mode: str = "neu") -> dict:
        """Insert ``code_str`` into the project.

        Parameters
        ----------
        code_str:
            The code block to insert.
        mode:
            Either ``"neu"`` to create a new block or ``"erweitern"`` to
            extend an existing one.

        Returns
        -------
        dict
            The result from :func:`safe_insert_code`.
        """

        return safe_insert_code(code_str, self.project_path, modus=mode)
