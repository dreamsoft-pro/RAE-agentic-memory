from unittest.mock import MagicMock, patch

import pytest

from sdk.rae_secure.client import RAEClient
from sdk.rae_secure.types import KernelResponse


class TestRAESecureClient:

    @pytest.fixture
    def mock_requests(self):
        with patch("sdk.rae_secure.client.requests.Session") as mock:
            yield mock

    def test_ask_sends_correct_payload(self, mock_requests):
        """Verify client constructs the correct JSON-RPC-like payload."""
        # Setup mock
        session_instance = mock_requests.return_value
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = {"success": True, "data": "test_response"}
        session_instance.post.return_value = response_mock

        # Init client
        client = RAEClient(kernel_url="http://mock-kernel", api_key="secret")

        # Execute
        result = client.ask("summarize", text="hello")

        # Assertions
        assert isinstance(result, KernelResponse)
        assert result.success is True
        assert result.data == "test_response"

        # Verify call arguments
        session_instance.post.assert_called_once()
        args, kwargs = session_instance.post.call_args
        assert args[0] == "http://mock-kernel/v1/agent/ask"
        payload = kwargs["json"]
        assert payload["name"] == "summarize"
        assert payload["parameters"]["text"] == "hello"

    def test_ask_handles_network_error(self, mock_requests):
        """Verify client returns failure response on network crash."""
        session_instance = mock_requests.return_value
        session_instance.post.side_effect = Exception("Connection refused")

        client = RAEClient()
        result = client.ask("ping")

        assert result.success is False
        assert "Connection refused" in result.error
