"""Utility for fetching URLs with logging."""

from __future__ import annotations

import requests

from utils.logger import get_logger

__all__ = ["fetch_url"]

logger = get_logger(__name__)


def fetch_url(url: str, *, timeout: int = 5) -> str | None:
    """Fetch the given URL and return its text content.

    Parameters
    ----------
    url: str
        The URL to request.
    timeout: int, optional
        Timeout for the request in seconds. Defaults to 5.

    Returns
    -------
    str | None
        The text of the response or ``None`` if an error occurred.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except Exception as exc:  # broad catch to log any request failure
        logger.error("Failed to fetch %s: %s", url, exc)
        return None
