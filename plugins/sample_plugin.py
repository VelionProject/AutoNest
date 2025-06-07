"""A sample plugin demonstrating the interface."""


def get_rules():
    def dummy_rule(matches, code_str, project_path):
        """Example rule doing nothing."""
        return matches

    return [dummy_rule]
