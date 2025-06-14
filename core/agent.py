"""Simple agent abstraction for AutoNest.

The agent acts as a thin wrapper around :class:`AutoNestEngine` and can be used
by CLI or GUI components to process user provided code blocks.
"""

from __future__ import annotations

from .engine import AutoNestEngine

__all__ = ["AutoNestAgent"]


class AutoNestAgent:
    """High level helper that delegates work to :class:`AutoNestEngine`."""

    def __init__(self, project_path: str) -> None:
        """Create an agent operating on ``project_path``."""

        self.engine = AutoNestEngine(project_path)

    def process(self, code_str: str, mode: str = "neu") -> dict:
        """Run suggestion and insertion for ``code_str``.

        Parameters
        ----------
        code_str:
            The new code snippet to insert or extend.
        mode:
            Insertion mode passed to :meth:`AutoNestEngine.insert`.

        Returns
        -------
        dict
            Mapping with ``suggestion`` and ``result`` entries.
        """

        suggestion = self.engine.suggest(code_str)
        result = self.engine.insert(code_str, mode)
        return {"suggestion": suggestion, "result": result}
