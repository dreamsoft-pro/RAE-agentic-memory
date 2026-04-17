import os
import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import yaml

# Import the function to test
import sys
from unittest.mock import MagicMock

# Mock out dependencies that might be missing or causing issues
sys.modules['anthropic'] = MagicMock()
sys.modules['anthropic.types'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['google.generativeai.types'] = MagicMock()
sys.modules['opentelemetry'] = MagicMock()
sys.modules['opentelemetry.trace'] = MagicMock()
sys.modules['opentelemetry.sdk.trace'] = MagicMock()
sys.modules['opentelemetry.exporter.otlp.proto.grpc.trace_exporter'] = MagicMock()

from orchestrator.intelligence.rae_integration import create_rae_integration

class TestRAEConfigLoading(unittest.TestCase):
    def setUp(self):
        # Clear environment variable for clean start
        if "RAE_ENDPOINT" in os.environ:
            del os.environ["RAE_ENDPOINT"]

    def test_default_fallback(self):
        """Test fallback to defaults when no config or env var is present."""
        with patch('pathlib.Path.exists', return_value=False):
            integration = create_rae_integration()
            self.assertIsNone(integration.rae_endpoint)
            self.assertEqual(integration.namespace, "orchestrator_performance")

    def test_env_var_fallback(self):
        """Test fallback to environment variable when no config is present."""
        os.environ["RAE_ENDPOINT"] = "http://env-endpoint:8000"
        with patch('pathlib.Path.exists', return_value=False):
            integration = create_rae_integration()
            self.assertEqual(integration.rae_endpoint, "http://env-endpoint:8000")
            self.assertEqual(integration.namespace, "orchestrator_performance")

    def test_config_file_loading(self):
        """Test loading from a specific config file."""
        config_content = {
            "rae": {
                "endpoint": "http://config-endpoint:8000",
                "namespace": "custom_namespace"
            }
        }
        yaml_str = yaml.dump(config_content)

        with patch("builtins.open", mock_open(read_data=yaml_str)):
            with patch("pathlib.Path.exists", return_value=True):
                integration = create_rae_integration(config_path="dummy.yaml")
                self.assertEqual(integration.rae_endpoint, "http://config-endpoint:8000")
                self.assertEqual(integration.namespace, "custom_namespace")

    def test_config_precedence_over_env(self):
        """Test that config file values take precedence over environment variables."""
        os.environ["RAE_ENDPOINT"] = "http://env-endpoint:8000"
        config_content = {
            "rae": {
                "endpoint": "http://config-endpoint:8000"
            }
        }
        yaml_str = yaml.dump(config_content)

        with patch("builtins.open", mock_open(read_data=yaml_str)):
            with patch("pathlib.Path.exists", return_value=True):
                integration = create_rae_integration(config_path="dummy.yaml")
                self.assertEqual(integration.rae_endpoint, "http://config-endpoint:8000")

if __name__ == "__main__":
    unittest.main()
