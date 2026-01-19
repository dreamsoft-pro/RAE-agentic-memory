import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

# Import the module to test
import importlib.util
spec = importlib.util.spec_from_file_location("bootstrap_session", "scripts/bootstrap_session.py")
bootstrap_session = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap_session)

def test_make_request_success():
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = json.dumps({"status": "healthy"}).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        code, data = bootstrap_session.make_request("http://test/health")
        assert code == 200
        assert data == {"status": "healthy"}

def test_get_active_url():
    # Patching the function directly on the loaded module object
    with patch.object(bootstrap_session, 'make_request') as mock_req:
        # Lumina offline, Local Dev online
        def side_effect(url, timeout=5):
            if "100.68.166.117" in url:
                return 0, {}
            if "localhost:8001" in url:
                return 200, {"status": "ok"}
            return 0, {}
            
        mock_req.side_effect = side_effect
        
        url = bootstrap_session.get_active_url()
        assert url == bootstrap_session.DEFAULT_URL

def test_fetch_context_success():
    with patch.object(bootstrap_session, 'make_request') as mock_req:
        mock_req.return_value = (200, {"results": [{"content": "test context", "layer": "working"}]})
        
        # Should not crash
        bootstrap_session.fetch_black_box_context("http://localhost:8001")
        assert mock_req.called

