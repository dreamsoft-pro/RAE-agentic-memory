import os
import sys
from unittest.mock import patch

import requests

# Allow importing from root directory
sys.path.append(os.getcwd())

from rae_agent.main import check_internet_leak, connect_to_kernel


class TestAgentRuntime:

    @patch("rae_agent.main.requests.get")
    def test_check_internet_leak_success(self, mock_get):
        """
        Isolation Success = Network Failure.
        The function checks if google.com is reachable.
        It returns True (Safe) if the request FAILS.
        """
        # Simulate Network Error (Good!)
        mock_get.side_effect = requests.exceptions.ConnectionError(
            "Network unreachable"
        )

        is_safe = check_internet_leak()
        assert is_safe is True

    @patch("rae_agent.main.requests.get")
    def test_check_internet_leak_fail_breach(self, mock_get):
        """
        Isolation Failure = Network Success.
        If google.com returns 200, the jail is broken.
        """
        # Simulate Success (Bad!)
        mock_get.return_value.status_code = 200

        is_safe = check_internet_leak()
        assert is_safe is False

    @patch("rae_agent.main.requests.get")
    def test_connect_to_kernel_success(self, mock_get):
        """Verify handshake with RAE Kernel."""
        mock_get.return_value.status_code = 200
        assert connect_to_kernel() is True

    @patch("rae_agent.main.requests.get")
    def test_connect_to_kernel_failure(self, mock_get):
        """Verify handshake failure handling."""
        mock_get.side_effect = Exception("Kernel down")
        assert connect_to_kernel() is False
