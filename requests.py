"""Minimal requests stub for offline testing."""

from types import SimpleNamespace


def get(*_args, **_kwargs):
    raise RuntimeError("requests not available in this environment")


class Response(SimpleNamespace):
    def raise_for_status(self):
        if getattr(self, "status_code", 200) >= 400:
            raise Exception(f"Status code {self.status_code}")
