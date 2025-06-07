"""A sample plugin demonstrating the plugin API.

This plugin filters out matches that point to ``__init__.py`` or reside inside
``tests`` directories.  Such locations are usually not ideal targets for new
functionality, so removing them from the result list can improve the automatic
selection.
"""

from __future__ import annotations

import os


def get_rules():
    def exclude_tests_and_init(matches, code_str, project_path):
        """Filter unwanted matches.

        Parameters
        ----------
        matches:
            List of match dictionaries produced by :func:`find_best_insertion_point`.
        code_str:
            The user supplied code snippet (unused).
        project_path:
            Base path of the analysed project (unused).

        Returns
        -------
        list
            The filtered match list. If all matches are filtered out, the
            original list is returned to avoid an empty result.
        """

        filtered = []
        for match in matches:
            file_path = os.path.normpath(match.get("file", ""))
            parts = file_path.split(os.sep)

            if os.path.basename(file_path) == "__init__.py":
                continue
            if "tests" in parts:
                continue
            filtered.append(match)

        return filtered or matches

    return [exclude_tests_and_init]
