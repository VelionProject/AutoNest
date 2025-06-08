import sys
import os
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import network_scanner


def test_fetch_url_success():
    expected_text = "hello"
    with mock.patch("requests.get") as mock_get:
        mock_response = mock.Mock()
        mock_response.text = expected_text
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = network_scanner.fetch_url("http://example.com")
    assert result == expected_text


def test_fetch_url_failure(caplog):
    with mock.patch("requests.get", side_effect=Exception("boom")):
        result = network_scanner.fetch_url("http://bad")
    assert result is None
    assert any("Failed to fetch" in record.message for record in caplog.records)
